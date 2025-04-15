import re

 
def read_config(filename):
    #dictionary to store the router_id and input_ports
    # read some file of router_id and input_ports
    router_txt=[]
    router_id = 0
    input_ports=[]
    output_ports=[]
    with open(filename, 'r') as file:
        lines = file.readlines()

        if not lines:
            raise ValueError("ERROR: Configuration file is empty.")
        
        for line in lines:
            line = re.split(', | |\n', line)
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
        expected_message = "ERROR: Invalid input port 1111111. Must be in range 1024-64000."
        assert str(e) == expected_message, f"Unexpected error message: {e}"
        print("Correct error raised:", e)

def test_invalid_router_id():
    config_filename = 'invalid_router_id.txt'
    try:
        config = read_config(config_filename)
    except ValueError as e:
        expected_message = "ERROR: router_id must be an integer."
        assert str(e) == expected_message, f"Unexpected error message: {e}"
        print("Correct error raised:", e)

def test_invalid_output_port():
    config_filename = 'invalid_output_port.txt'
    try:
        config = read_config(config_filename)
    except ValueError as e:
        expected_message = "ERROR: Invalid output-port format"
        assert str(e) == expected_message, f"Unexpected error message: {e}"
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