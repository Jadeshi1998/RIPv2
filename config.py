import socket
import sys
import threading
import re

def read_config(filename):
    # read some file of router_id and input_ports
    # config={router_id=None, input_ports=[], outputs=[]}
    lines=[]
    file=open(filename,'r')
    for line in file.readlines():
        line = re.split(', | |\n',line)
        print(line)
        lines.append(line)
    print(lines)

