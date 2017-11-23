#!/usr/bin/env python
""" Insert description of this program here """

import tmutil, sys, os
import tmglobals
globals = tmglobals.tmglobals()



### Insert classes and functions here.  The main program begins in the "if" statement below.
def dumpit(curs):
    for (title, content) in curs.fetchall():
        with open(title+'.html', 'w') as outfile:
            outfile.write(content.replace('\r\n','\n'))
            if content[-1] != '\n':
                outfile.write('\n')

if __name__ == "__main__":
    os.chdir('data')
    import dbconn
    conn = dbconn.dbconn(dbname='joomla',dbuser='david',dbpass='xyzzy')
    curs = conn.cursor()
    curs.execute("select title, content from ujln1_modules where title like '%level%' and published = 1")
    dumpit(curs)

    curs.execute("select title, introtext from ujln1_content where title like '%path%' and state = 1");
    dumpit(curs)


    
