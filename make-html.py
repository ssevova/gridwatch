#!/bin/env python

from argparse import ArgumentParser
from subprocess import check_output
import datetime


def getArguments():
    parser = ArgumentParser()
    parser.add_argument("production")
    parser.add_argument("-p", "--prefix", default="group.phys-exot")
    parser.add_argument("-u", "--user", default="Philipp Gadow")
    return parser

def getInfo(production, prefix, user):
    out = check_output(["/eos/user/p/pgadow/www/gridwatch/pandamon", "-u", str(user), "-d", "90", str(prefix) + "*" + str(production) + "*.EXOT27"])
    out = out.split("\n")
    out = [line.split() for line in out]
    return out

def getStatusColour(status):
    if status == 'ready': return '#D3D3D3' # light gray
    elif status == 'broken': return '#B22222' # firebrick red
    elif status == 'done': return '#006400' # dark green
    elif status == 'running': return '#32CD32' # limegreen
    elif status == 'scouting': return '#20B2AA' # light seagreen
    return '#2F4F4F' # dark slategray

def writeHTML(info, production, user):
    with open('/eos/user/p/pgadow/www/gridwatch/monosww_'+production+'.html', 'w') as outFile:
        # write HTML header
        outFile.write("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Mono-s(WW) ntuple creation tag {production}</title>
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  </head>
  <body>
  <div class="container">
    <h1>Mono-s(WW) ntuple generation</h1> 
  <p>Last updated: {date}</p> 
</div>
    <table style="width:100%">
""".format(date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), production=production))
        # write HTML table
        for line in sorted(info):
            if not line: continue
            outFile.write("""

  <tr>
    <th><font color="{fontcolour}">{status}</font></th>
    <th>{percent}</th> 
    <th><a href="https://bigpanda.cern.ch/tasks/?reqid={taskid}&username={user}&days=180">{name}</a></th>
  </tr>
""".format(status=line[0], percent=line[2], name=line[3], taskid=line[1], user=user.replace(' ', '%20'), fontcolour=getStatusColour(line[0])))

        # write HTML footer
        outFile.write("""
    </table>
  </body>
</html>
""")

def main():
    args = getArguments().parse_args()
    production = args.production
    prefix = args.prefix
    user = args.user
    info = getInfo(production, prefix, user)
    writeHTML(info, production, user)

if __name__ == "__main__":
    main()

