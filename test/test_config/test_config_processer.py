import re

 
def read_config(filename):
    #dictionary to store the router_id and input_ports
    # read some file of router_id and input_ports
    router_txt=[]
    router_id = 0
    input_ports=[]
    output_ports=[]
    file=open(filename,'r')
    lines = file.readlines()

    if not lines:
        raise ValueError("ERROR: Configuration file is empty.")
    
    for line in file.readlines():
        line = re.split(', | |\n',line)
        router_txt.append(line)

    try:
        router_id = int(router_txt[0][1])
    except ValueError:
        raise ValueError("ERROR: router_id must be an integer.")
    if not (1 <= router_id <= 64000):
        raise ValueError(f"ERROR: Invalid router ID {router_id}. Must be in range 1-64000.")

    for port in router_txt[1][1:-1]:
        if not (1024 <= int(port) <= 64000):
            raise ValueError(f"ERROR: Invalid input port {port}. Must be in range 1024-64000.")
        input_ports.append(int(port))

    #get output_ports
    for port in router_txt[2][1:-1]:
        port = re.split('-',port)
        if len(port) != 3:
            raise ValueError(f"ERROR: Invalid output-port format") 
        if not (1024 <= int(port[0]) <= 64000):
            raise ValueError(f"ERROR: Invalid output port {port[0]}. Must be in range 1024-64000.")
        output_ports.append([int(port[0]),int(port[1]),int(port[2])])

    config= {
    'router_id': router_id,
    'input_ports': input_ports,
    'output_ports': output_ports
    }
    return config
    

##########################test cases#########################
def good_test():
    config_filename = 'router4.txt'  
    config = read_config(config_filename)
    print(config)
    # {'router_id': 4, 'input_ports': [4441, 4442, 4443], 'output_ports': [[3332, 4, 3], [7772, 6, 7], [5551, 2, 5]]}

def test_invalid_input_port():
    config_filename = 'invalid_input_port.txt'  
    config = read_config(config_filename)
    print(config)
    #ValueError: ERROR: Invalid input port 1111111. Must be in range 1024-64000.

def test_invalid_router_id():
    config_filename = 'invalid_router_id.txt'
    config = read_config(config_filename)
    print(config)
    #ValueError: ERROR: router_id must be an integer.
    
def test_invalid_output_port():
    config_filename = 'invalid_output_port.txt'
    config = read_config(config_filename)   
    print(config)
    #ValueError: ERROR: Invalid output-port format

def test_empty():
    config_filename = 'empty.txt'
    config = read_config(config_filename)
    print(config)
    #ValueError: ERROR: Configuration file is empty.

#good_test()
#test_invalid_input_port()
#test_invalid_router_id()
#test_invalid_output_port()
test_empty()