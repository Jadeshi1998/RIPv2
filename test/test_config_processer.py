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
    #print(f"Router text : {router_txt}")

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
            # check port[0]
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
                #check_same_ports.append(port[0])
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

#test()
##########################test cases#########################
def test_router1():
    config_filename = 'router1.txt'  
    config = read_config(config_filename)
    assert config == {'router_id': 1, 'input_ports': [1111, 1112, 1113], 'output_ports': [[2221, 1, 2], [6661, 5, 6], [7771, 8, 7]]}
    print("router1 pass.")

def test_router2():
    config_filename = 'router2.txt'  
    config = read_config(config_filename)
    assert config == {'router_id': 2, 'input_ports': [2221, 2222], 'output_ports': [[1111, 1, 1], [3331, 3, 3]]}
    print("router3 pass.")

def test_router3():
    config_filename = 'router3.txt'  
    config = read_config(config_filename)
    assert config == {'router_id': 3, 'input_ports': [3331, 3332], 'output_ports': [[2222, 3, 2], [4441, 4, 4]]}
    print("router3 pass.")

def test_router4():
    config_filename = 'router4.txt'  
    config = read_config(config_filename)
    assert config == {'router_id': 4, 'input_ports': [4441, 4442, 4443], 'output_ports': [[3332, 4, 3], [7772, 6, 7], [5551, 2, 5]]}
    print("router4 pass.")

def test_router5():
    config_filename = 'router5.txt'  
    config = read_config(config_filename)
    assert config == {'router_id': 5, 'input_ports': [5551, 5552], 'output_ports': [[4442, 2, 4], [6662, 1, 6]]}
    print("router5 pass.")

def test_router6():
    config_filename = 'router6.txt'  
    config = read_config(config_filename)
    assert config == {'router_id': 6, 'input_ports': [6661, 6662], 'output_ports': [[1112, 5, 1], [5552, 1, 5]]}
    print("router6 pass.")

def test_router7():
    config_filename = 'router7.txt'  
    config = read_config(config_filename)
    assert config == {'router_id': 7, 'input_ports': [7771, 7772], 'output_ports': [[1113, 8, 1], [4443, 6, 4]]}
    print("router7 pass.")

def test_invalid_input_port():
    config_filename = 'invalid_input_port.txt'
    try:
        config = read_config(config_filename)
    except ValueError as e:
        expected_message = "ERROR: Invalid input_ports format, input_ports must be less than 64000, not 1111111"
        assert str(e) == expected_message
        print("Correct error raised:", e)

def test_invalid_router_id():
    config_filename = 'invalid_router_id.txt'
    try:
        config = read_config(config_filename)
    except ValueError as e:
        expected_message = "ERROR: Invalid router_id format, router_id must be not an alphabetic string, not abc"
        assert str(e) == expected_message
        print("Correct error raised:", e)

def test_invalid_output_port():
    config_filename = 'invalid_output_port.txt'
    try:
        config = read_config(config_filename)
    except ValueError as e:
        expected_message = "ERROR: Invalid output-port format, must be 'output-ports <peer_port> <metric> <peer_ID>'"
        assert str(e) == expected_message
        print("Correct error raised:", e)

def test_empty():
    config_filename = 'empty.txt'
    try:
        config = read_config(config_filename)
    except ValueError as e:
        expected_message = "ERROR: Configuration file is empty."
        assert str(e) == expected_message, f"Unexpected error message: {e}"
        print("Correct error raised:", e)


test_router1()
test_router2()
test_router3()
test_router4()
test_router5()
test_router6()
test_router7()
test_invalid_input_port()
test_invalid_router_id()
test_invalid_output_port()
test_empty()