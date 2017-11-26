#!/usr/bin/env python3
from __future__ import print_function
import xlrd
import os,sys

class Path:
    paths = {}
    @classmethod
    def get(self, name):
        if name not in self.paths:
            self.paths[name] = Path(name)
            
        return self.paths[name]
        
    def __init__(self, name):
        self.name = name
        self.projects = []
        self.blurb = ''

class Project:
    def __init__(self, name, order, path, value):
        self.name = name
        self.order = order
        self.value = value
        self.level = int(self.value[0])
        self.required = 'R' in self.value
        self.key = (self.level, not self.required, self.value, self.order)
        Path.get(path).projects.append(self)
        
levels = {1: "Mastering Fundamentals",
          2: "Learning Your Style",
          3: "Increasing Knowledge",
          4: "Building Skills",
          5: "Demonstrating Expertise"}

book = xlrd.open_workbook('Projects.xlsx')
os.chdir('data')

# Get the projects
sheet = book.sheet_by_name('Projects')
colnames = sheet.row_values(0)

# Create paths
namecol = colnames.index('Name')
ordercol = colnames.index('Order')
pathcols = range(namecol+1,sheet.ncols)


# Create projects and assign to paths
for rownum in range(1,sheet.nrows):
    order = sheet.cell_value(rownum, ordercol)
    if not order:
        order = 0
    name = sheet.cell_value(rownum, namecol)
    for p in pathcols:
        val = ('%s' % sheet.cell_value(rownum, p)).strip()
        if val:
            Project(name, order, colnames[p], val)
            
# Now, get the blurbs for each path
sheet = book.sheet_by_name('Paths')
for rownum in range(1, sheet.nrows):
    pathname = sheet.cell_value(rownum, 0)
    path = Path.get(pathname)
    path.blurb = sheet.cell_value(rownum, 1)
            
# OK, now create the output

for p in pathcols:
    pathname = colnames[p]
    pathid = ''.join([part[0:4] for part in pathname.lower().split()[0:2]])
    path = Path.get(pathname)
    path.projects.sort(key=lambda item:item.key)
    with open('Path ' + pathname + '.html', 'w', encoding='utf-8') as outfile:
        outfile.write("""    <style type="text/css">
    .pathname {font-size: 175%; font-weight: bold; background: #004165; color: white; padding: 3px;}
    .level {font-size: 150%; font-weight: bold; background: #f2df7480; margin-top: 1em; padding: 3px; margin-bottom: 0.5em;}
    .projname {font-size: 125%; font-weight: bold; color: #772432}
    .electives {background: #00416520; }
    .electives-header {font-size: 135%; font-weight: bold; background: #00416520; color: black; margin-top: 1em; padding-bottom: 0.5em;}
    .projdesc {margin-bottom: 2em;}
    </style>
""")
        outfile.write('<h2 class="pathname">%s</h2>\n' % pathname)
        outfile.write('<p class="blurb">%s</p>\n' % path.blurb)
        level = 0
        inelectives = False
        for item in path.projects:
            if item.level != level:
                if inelectives:
                  outfile.write('</div --electives-->\n')
                outfile.write('<h3 class="level">Level %s: %s</h3>\n' % (item.level, levels[item.level]))
                level = item.level
                inelectives = False
                itemnum = 0
            itemnum += 1
            itemid = '%s%s%s' % (pathid, level, itemnum)
            if not inelectives and not item.required:
                outfile.write('<div class="electives-header">Electives (Choose %d)</div>\n' % [0, 0, 0, 2, 1, 1][level])   
                outfile.write('<div class="electives">\n')
                inelectives = True
            outfile.write('<div class="%s-project">\n' % ('req' if item.required else 'elective'))

            outfile.write('<div class="projname" onclick="jQuery(\'#%sopen, #%sclosed, #%sdesc\').toggle()">' % (itemid, itemid, itemid))
            outfile.write('<span id="%sopen" style="display:none">&#x2296;</span><span id="%sclosed">&#x2295;</span> %s\n' % (itemid, itemid, item.name)) 
            outfile.write('</div --projname-->\n')
            outfile.write('<div id="%sdesc" class="projdesc" style="display:none;">\n' % itemid)
            outfile.write(open(item.name+'.html', 'r', encoding='utf-8').read().encode('ascii','xmlcharrefreplace').decode())
            outfile.write('</div  --projdesc-->\n')
            outfile.write('</div --whatever-project-->\n')
        if inelectives:
            outfile.write('</div --electives-->\n')
        

    
            

    