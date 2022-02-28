import sys
import os
import subprocess

for filename in os.listdir():
    if os.path.isfile(filename):
        if filename.startswith('board'):
            goal = filename.replace('.agda','.html')
            if not os.path.isfile(goal):
                if os.path.isfile('chalkboard.agda'):
                    os.unlink('chalkboard.agda')
                if os.path.isfile('html/chalkboard.html'):
                    os.unlink('html/chalkboard.html')

                f = open(filename, 'r')
                g = open('chalkboard.agda', 'w')
                for line in f.readlines():
                    line = line.replace('--cubical','--cubical --allow-unsolved-metas')
                    g.write(line)
                f.close()
                g.close()
                
                subprocess.run(["agda", "--html", "chalkboard.agda"])
                if os.path.isfile('html/chalkboard.html'):
                    os.rename('html/chalkboard.html',goal)
