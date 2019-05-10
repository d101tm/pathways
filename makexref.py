#!/usr/bin/env python3
from __future__ import print_function
from googleapiclient import discovery
import os,sys
from credentials import apikey

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
    def __init__(self, name, path, value):
        self.name = name
        self.value = value
        self.level = int(self.value[0])
        self.required = 'R' in self.value
        self.isIceBreaker = self.name == 'Ice Breaker'
        self.key = (self.level, not self.isIceBreaker, not self.required, self.value, self.name)
        Path.get(path).projects.append(self)
    
        
levels = {1: "Mastering Fundamentals",
          2: "Learning Your Style",
          3: "Increasing Knowledge",
          4: "Building Skills",
          5: "Demonstrating Expertise"}
        
styleinfo = """    <style type="text/css">
    .pathname-header {font-size: 175%; font-weight: bold; background: #004165; color: white; padding: 3px; margin-top: 2em; margin-bottom: 0.5em;}
    .level {font-size: 150%; font-weight: bold; background: #f2df7480; margin-top: 1em; padding: 3px; margin-bottom: 0.5em;}
    .projname {font-size: 125%; font-weight: bold; color: #772432}
    .electives {background: #00416520; }
    .electives-header {font-size: 135%; font-weight: bold; background: #00416520; color: black; margin-top: 1em; padding-bottom: 0.5em;}
    .projdesc {margin-bottom: 2em;}
    </style>
"""

def cleanup(s):
    """Remove extraneous newlines (all not before a tag)"""
    return s.replace('\n<', '\x00').replace('\n',' ').replace('\x00','\n<').strip()

# Connect to the Google Spreadsheet with path and project info
service = discovery.build('sheets','v4',developerKey=apikey)
sheetid = '199fHCu4LJ9UvJJCCiNpytvoHn0kxQJXSm93Z_-EFPW0'
request = service.spreadsheets().values()

# Get the projects
result = request.get(spreadsheetId=sheetid, range='Projects').execute().get('values',[])
colnames = result[0]   

# Create paths
namecol = colnames.index('Name')
pathcols = range(namecol+1,len(colnames))


# Create projects and assign to paths
for row in result[1:]:
    name = row[namecol]
    for p in pathcols:
        try:
            val = ('%s' % row[p]).strip()
        except IndexError:
            val = ''
        if val:
            Project(name, colnames[p], val)
            
# Now, get the blurbs for each path
result = request.get(spreadsheetId=sheetid, range='Paths').execute().get('values',[])
for row in result[1:]:
    pathname = row[0]
    path = Path.get(pathname)
    path.blurb = row[1]
            
# OK, now create the output
outfile = open(os.path.join("output", "allpaths.html"), "w", encoding="utf-8")
outfile.write(styleinfo)


for p in pathcols:
    pathname = colnames[p]
    pathid = ''.join([part[0:4] for part in pathname.lower().split()[0:2]])
    path = Path.get(pathname)
    path.projects.sort(key=lambda item:item.key)
    outfile.write('<div class="pathname-header">\n')
    # Write the expandable header 
    outfile.write('<div class="pathname" onclick="jQuery(\'#%sopen, #%sclosed, #%sdesc\').toggle()">' % (pathid, pathid, pathid))
    outfile.write('<span id="%sopen" style="display:none">&#x2296;</span><span id="%sclosed">&#x2295;</span> %s\n' % (pathid, pathid, pathname)) 
    outfile.write('</div>\n')
    outfile.write('</div>')  # Close the pathname header
    outfile.write('<p class="blurb">%s</p>\n' % path.blurb)
    
    # Write the wrapper 
    outfile.write('<div id="%sdesc" style="display:none">\n' % pathid)
    
    # Write the details
    level = 0
    inelectives = False
    for item in path.projects:
        if item.level != level:
            if inelectives:
                outfile.write('</div>\n')
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
        outfile.write('</div>\n')
        outfile.write('<div id="%sdesc" class="projdesc" style="display:none;">\n' % itemid)
        outfile.write(cleanup(open('projects/'+item.name+'.html', 'r', encoding='utf-8').read().encode('ascii','xmlcharrefreplace').decode()))
        outfile.write('</div>\n')
        outfile.write('</div>\n')
    if inelectives:
        outfile.write('</div>\n')
    
    # Close the wrapper
    outfile.write('</div>\n')  


            

    
