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
    print("get router")
    print(router_txt)
    
    #get input_ports
    for port in router_txt[1][1:-1]:
        if not (1024 <= int(port) <= 64000):
            raise ValueError(f"ERROR: Invalid input port {port}. Must be in range 1024-64000.")
        # print(port)
        input_ports.append(port)
    print("get input_ports")    
    print(input_ports)
 
    #get output_ports
    for port in router_txt[2][1:-1]:
        port = re.split('-',port)
        if not (1024 <= int(port[0]) <= 64000):
            raise ValueError(f"ERROR: Invalid output port {port[0]}. Must be in range 1024-64000.")
        output_ports.append(port)
    print("get output_ports")
    print(output_ports)

    #make a dictionary of table of router
    table = {}
    for output_port in output_ports:
        metric= int(output_port[1])
        id = int(output_port[2])
        next_hop = int(output_port[0])
        flag = False
        time_out = 0
        garbage_time = 0
        table[id] = [metric,next_hop,flag,time_out,garbage_time]
       
    print("get table")
    print(table)


    return table
    
    


def main():
    config_filename = 'router1.txt'  
    read_config(config_filename)

#  #去掉就能跑了 文件可以单独测试 not# will run
# if __name__ == "__main__":
#     main()