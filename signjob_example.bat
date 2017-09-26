

set py="python"
rem login first
%py% scripts/fh_network.py

start /b cmd /c %py% scripts/signin.py -u xx -p xx -m xx@fiberhome.com -g xx
%py% scripts/sleep.py 2
start /b cmd /c %py% scripts/signin.py -u xx -p xx-m xx@fiberhome.com -g xx,xx