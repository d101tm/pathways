from __future__ import print_function
from awardinfo import Awardinfo
import sys

s = Awardinfo()
idlist = ['paths']
out = ['<div id="paths">']
out.append('  <ul>')
for p in sorted(s.pathids):
    pid = p.lower()
    out.append('    <li><a href="#%s">%s</a></li>' % (pid, s.pathids[p]))
out.append('  </ul>')


for p in sorted(s.pathids):
    pid = p.lower()
    out.append('  <div id="%s">' % pid)
    out.append('    <p>This is the section about %s' % s.pathids[p])
    out.append('    <div id="%slevels">' % pid)
    idlist.append('%slevels' % pid)
    out.append('      <ul>')
    levels = []
    for i in [1, 2, 3, 4, 5]: 
        out.append('      <li><a href="#%s%d">Level %d</a></li>' % (pid, i, i))
        levels.append('      <div id="%s%d">' % (pid, i))
        levels.append('        <p>This is the section about %s Level %d' % (s.pathids[p], i))
        levels.append('      </div>')
    out.append('      </ul>')
    out.extend(levels)
    out.append('  </div>')

    out.append('  </div>')
    
print('\n'.join(out))
sys.exit(0)
print("""
    <script>
    $(function() {
""")
for item in idlist:
    print('      $("#%s").tabs();' % item)
print("""
    } );
    </script>
""")
      

