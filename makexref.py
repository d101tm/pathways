#!/usr/bin/env python
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
            
for p in pathcols:
    pathname = colnames[p]
    path = Path.get(pathname)
    print(pathname)
    path.projects.sort(key=lambda item:item.key)
    for item in path.projects:
        print("%40s Level %s %s" % (item.name, item.level, "Required" if item.required else ""))
    
            

    