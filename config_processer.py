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
    if router_txt == []:
        raise ValueError("ERROR: Invalid router config file, empty file")
    if len(router_txt) != 3:
        raise ValueError("ERROR: Invalid router config file, must be 3 lines")

    #get router_id
    router_id=check_router_id(router_txt[0])
    #print(f"Router_id : {router_id}")
    

    #get input_ports
    input_ports=check_input_ports(router_txt[1])
    #print(f"Input_ports : {input_ports}")

    #get output_ports
    output_ports=check_output_ports(router_txt[2],input_ports)
    #print(f"Output_ports = [peer_port, metric, peer_ID]: {output_ports}")

    config= {
    'router_id': router_id,
    'input_ports': input_ports,
    'output_ports': output_ports
    }
    return config
    
def check_router_id(line):
        if len(line) != 3:
            raise ValueError("ERROR: Invalid router_id format, must be 'router_id <router_id>'")
        if line[0] != 'router-id':
            raise ValueError(f"ERROR: Invalid router_id format, must be 'router_id <router_id>', not {line[0]}")
        if line[1].isalpha():
            raise ValueError(f"ERROR: Invalid router_id format, router_id must be not an alphabetic string, not {line[1]}")
        if line[1].isdigit():
            if int(line[1])<=0:
                raise ValueError(f"ERROR: Invalid router_id format, router_id must be more than zero, not {line[1]}")
            if int(line[1])>64000:
                raise ValueError(f"ERROR: Invalid router_id format, router_id must be less than 64000, not {line[1]}")
            line[1] = int(line[1])
        else:
            if line[1].startswith('-'):
                raise ValueError(f"ERROR: Invalid router_id format, router_id must be positive integer, not {line[1]}")
            raise ValueError(f"ERROR: Invalid router_id format, router_id must be an integer, not {line[1]}")
        return line[1]
def check_input_ports(line):
        input_list = []
        if len(line) <= 2:
            raise ValueError("ERROR: Invalid input_ports format, At least one input port is required")
        if line[0] != 'input-ports':
            raise ValueError(f"ERROR: Invalid input_ports format, the first one is 'input-ports', not {line[0]}")
        for port in line[1:-1]:
            if port.isalpha():
                raise ValueError(f"ERROR: Invalid input_ports format, input_ports must be not an alphabetic string, not {port}")
            if port.isdigit():
                if int(port)<1024:
                    raise ValueError(f"ERROR: Invalid input_ports format, input_ports must be more then 1024, not {port}")
                if int(port)>64000:
                    raise ValueError(f"ERROR: Invalid input_ports format, input_ports must be less than 64000, not {port}")
                input_list.append(int(port))
            else:
                if port.startswith('-'):
                    raise ValueError(f"ERROR: Invalid input_ports format, input_ports must be more than 1024 and not negative, not {port}")
                raise ValueError(f"ERROR: Invalid input_ports format, input_ports must be an integer, not {port}")
        if len(input_list) !=len(set(input_list)):
            raise ValueError(f"ERROR: Invalid input_ports format, input_ports must be unique")
        return input_list

def check_output_ports(line,input_ports):
        output_list = []
        check_same_ports = []
        if len(line) <= 2:
            raise ValueError("ERROR: Invalid output_ports format, At least one output port is required")
        if line[0] != 'output-ports':
            raise ValueError(f"ERROR: Invalid output_ports format, the first one is 'output-ports', not {line[0]}")
        
        for port in line[1:-1]:
            port = re.split('-',port)
            if len(port) != 3:
                raise ValueError(f"ERROR: Invalid output-port format, must be 'output-ports <peer_port> <metric> <peer_ID>'")
            if port[0].isalpha() or port[1].isalpha() or port[2].isalpha():
                raise ValueError(f"ERROR: Invalid output_ports format, output_ports must be not an alphabetic string, not {port}")

            # check port[1]
            if port[1].isdigit():
                if int(port[1])<0:
                    raise ValueError(f"ERROR: Invalid output_ports format, metric must be more then 0, not {port[1]}")
                if int(port[1])>16:
                    raise ValueError(f"ERROR: Invalid output_ports format, metric must be less than 16, not {port[1]}")
                port[1] = int(port[1])
            # check port[2]
            if port[2].isdigit():
                if int(port[2])<=0:
                    raise ValueError(f"ERROR: Invalid output_ports format, router_id must be more than zero, not {port[2]}")
                if int(port[2])>64000:
                    raise ValueError(f"ERROR: Invalid output_ports format, router_id must be less than 64000, not {port[2]}")
                port[2] = int(port[2])
            else:
                if line[1].startswith('-'):
                    raise ValueError(f"ERROR: Invalid output_ports format, router_id must be positive integer, not {port[2]}")
                raise ValueError(f"ERROR: Invalid output_ports format, router_id must be an integer, not {port[2]}")
            # check port[0]
            if port[0].isdigit():
                if int(port[0])<1024:
                    raise ValueError(f"ERROR: Invalid output_ports format, port must be more then 1024, not {port[0]}")
                if int(port[0])>64000:
                    raise ValueError(f"ERROR: Invalid output_ports format, port must be less than 64000, not {port[0]}")
                if int(port[0]) in input_ports:
                    raise ValueError(f"ERROR: Invalid output_ports format, port must not be the same as input_ports, not {port[0]}")
                for i in check_same_ports:
                    if int(port[0]) == int(i):
                        raise ValueError(f"ERROR: Invalid output_ports format, port must be unique, {port[0]} is already used")
               
                check_same_ports.append(port[0])
 
            else:
                if port[0].startswith('-'):
                    raise ValueError(f"ERROR: Invalid output_ports format, port must be positive integer, not {port[0]}")
                raise ValueError(f"ERROR: Invalid output_ports format, port must be an integer, not {port[0]}")
            # make output_list

            output_list.append([int(port[0]),int(port[1]),int(port[2])])
        
           
        return output_list

def test():
    config_filename = 'router1.txt'  
    config = read_config(config_filename)
    print(config)

test()