import sys
for line in sys.stdin:
    tok=line.split("\t")
    if tok[1]!='<h>':
        sys.stdout.write(tok[-1]+'\n')
