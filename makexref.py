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

class Project:
    def __init__(self, name, order, path, value):
        self.name = name
        self.order = order
        self.value = value
        self.level = int(self.value[0])
        self.required = 'R' in self.value
        self.key = (self.level, not self.required, self.value, self.order)
        Path.get(path).projects.append(self)
        

book = xlrd.open_workbook('Projects.xlsx')
os.chdir('data')
sheet = book.sheet_by_index(0)
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
            
# OK, now create the output

for p in pathcols:
    pathname = colnames[p]
    pathid = ''.join([part[0:4] for part in pathname.lower().split()[0:2]])
    path = Path.get(pathname)
    path.projects.sort(key=lambda item:item.key)
    with open('Path ' + pathname + '.html', 'w', encoding='utf-8') as outfile:
        outfile.write("""    <script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
    <script>
        jQ = jQuery.noConflict();
    </script>
    <style type="text/css">
    </style>
    """)
        outfile.write('<h2>%s</h2>' % pathname)
        level = 0
        electives = []
        for item in path.projects:
            if item.level != level:
                outfile.write('<h3>Level %s</h3>' % item.level)
                level = item.level
                inelectives = False
                itemnum = 0
            itemnum += 1
            itemid = '%s%s%s' % (pathid, level, itemnum)
            if item.required:
                outfile.write('<div class="req-project">\n')
                outfile.write('<div class="projname">%s</div>\n' % item.name)
            elif not inelectives:
                outfile.write('<h4>Electives (Choose %d)</h4>\n' % [0, 0, 0, 2, 1, 1][level])   
                inelectives = True
            if not item.required:
                outfile.write('<div class="elective-project" id="%s">\n' % itemid)
                outfile.write('<div class="projname" onclick="jQ(\'#%sopen, #%sclosed, #%sdesc\').toggle()">' % (itemid, itemid, itemid))
                outfile.write('<span id="%sopen" style="display:none">&#x25be; %s</span>\n' % (itemid, item.name)) 
                outfile.write('<span id="%sclosed">&#x25b8; %s</span>' % (itemid, item.name))
                outfile.write('<div id="%sdesc" style="display:none;">\n' % itemid)
            outfile.write(open(item.name+'.html', 'r', encoding='utf-8').read().encode('ascii','xmlcharrefreplace').decode())
            if not item.required:
                outfile.write('</div>\n')
            outfile.write('</div>\n')
        

    
            

    