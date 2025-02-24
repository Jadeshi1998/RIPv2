import socket
import sys
import threading
import re

def read_config(filename):
    # read some file of router_id and input_ports

    router_txt=[]
    input_ports=[]
    output_ports=[]
    file=open(filename,'r')
    for line in file.readlines():
        line = re.split(', | |\n',line)
        router_txt.append(line)
    print(router_txt)
    
    #get input_ports
    for port in router_txt[1][1:-1]:
        if not (1024 <= int(port) <= 64000):
            raise ValueError(f"ERROR: Invalid input port {port}. Must be in range 1024-64000.")
        # print(port)
        input_ports.append(port)
    print(input_ports)
 
    #get output_ports
    for port in router_txt[2][1:-1]:
        port = re.split('-',port)
        if not (1024 <= int(port[0]) <= 64000):
            raise ValueError(f"ERROR: Invalid output port {port[0]}. Must be in range 1024-64000.")
        output_ports.append(port)
    print(output_ports)
    


def main():
    config_filename = 'router1.txt'  
    read_config(config_filename)

if __name__ == "__main__":
    main()