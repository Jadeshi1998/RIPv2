import socket
import sys
import threading
import re

 
def read_config(filename):
    #dictionary to store the router_id and input_ports
    # read some file of router_id and input_ports
    router_txt=[]
    router_id = 0
    input_ports=[]
    output_ports=[]
    file=open(filename,'r')
    for line in file.readlines():
        line = re.split(', | |\n',line)
        router_txt.append(line)
    print(f"Router text : {router_txt}")

    #get router_id
    try:
        router_id = int(router_txt[0][1])
    except ValueError:
        raise ValueError("ERROR: router_id must be an integer.")
    if not (1 <= router_id <= 64000):
        raise ValueError(f"ERROR: Invalid router ID {router_id}. Must be in range 1-64000.")
    print(f"Router ID : {router_id}")

    #get input_ports
    for port in router_txt[1][1:-1]:
        if not (1024 <= int(port) <= 64000):
            raise ValueError(f"ERROR: Invalid input port {port}. Must be in range 1024-64000.")
        # print(port)
        input_ports.append(int(port))
    print(f"Input_ports : {input_ports}")
    
    #get output_ports
    for port in router_txt[2][1:-1]:
        port = re.split('-',port)
        if len(port) != 3:
            raise ValueError(f"ERROR: Invalid output-port format") 
        if not (1024 <= int(port[0]) <= 64000):
            raise ValueError(f"ERROR: Invalid output port {port[0]}. Must be in range 1024-64000.")
        output_ports.append([int(port[0]),int(port[1]),int(port[2])])
    print(f"Output_ports = [peer_port, metric, peer_ID]: {output_ports}")

    config= {
    'router_id': router_id,
    'input_ports': input_ports,
    'output_ports': output_ports
    }
    return config
    

def test():
    config_filename = 'router4.txt'  
    config = read_config(config_filename)
    #print(config)

#test()