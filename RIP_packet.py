"""
    RIP Packet Structure

        0                   1                   2                   3  
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1  
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | command : 1/2   | version : 2  |      must be zero (2)       |
    +---------------+---------------+-------------------------------+
    |                  RIP Entry (20 bytes)                        |
    |                 (May repeat multiple times)                  |
    |                [(metric, destination),()...]                 |
    +---------------------------------------------------------------+
    command = 1 for request, 2 for response
    version = 2
"""
COMMAND_REQUEST = 1
COMMAND_RESPONSE = 2
VERSION = 2
METRIC_INFINITY = 16
def RIP_header(router_id):
    """Build up rip packet header and entry"""
    # rip packet header = [command, version, source]
    source = router_id
    command = COMMAND_REQUEST
    header = [command, VERSION, source]
    header_rep = f'command : {command}, version : {VERSION}, source : {source}'
    return header,header_rep

def RIP_entry(table):
    # 
    entry = []
    
    for num in range(len(table)):
        next_port = table[num][0]
        cost = table[num][1]
        next_hop = table[num][2]
        entry.append([next_port,cost, next_hop]) 
        if not (1 <= cost < METRIC_INFINITY):
            raise ValueError(f"ERROR: Invalid metric {cost}. Must be in range 1-15.")
        print(f'next_port:{next_port}, cost : {cost}, next_hop :{next_hop}')
    return entry

def rip_packet(router_id, table):
    """Full RIP packet."""
    header = RIP_header(router_id)
    entries = RIP_entry(table)
    packet = [header, entries]
    return packet



def test_rip_packet():
    # Test 1: Basic Valid Packet
    try:
        router_id = 1
        table = [[6, 1, 2], [5, 2, 3], [4, 3, 4]]
        packet = rip_packet(router_id, table)
        print("Test 1 Passed: Basic Valid Packet")
    except Exception as e:
        print(f"Test 1 Failed: {e}")

    # Test 2: Invalid Metric
    try:
        router_id = 1
        table = [[6, 0, 2]]  # Invalid metric
        packet = rip_packet(router_id, table)
        print("Test 2 Failed: Invalid Metric not caught")
    except ValueError as e:
        print("Test 2 Passed: Invalid Metric caught")

    # Test 3: Empty Routing Table
    try:
        router_id = 1
        table = []
        packet = rip_packet(router_id, table)
        print("Test 3 Passed: Empty Routing Table")
    except Exception as e:
        print(f"Test 3 Failed: {e}")

    # Test 4: Maximum Metric
    try:
        router_id = 1
        table = [[6, 15, 2]]
        packet = rip_packet(router_id, table)
        print("Test 4 Passed: Maximum Metric")
    except Exception as e:
        print(f"Test 4 Failed: {e}")

    # Test 5: Multiple Entries
    try:
        router_id = 1
        table = [[6, 1, 2], [5, 2, 3], [4, 3, 4], [3, 4, 5]]
        packet = rip_packet(router_id, table)
        print("Test 5 Passed: Multiple Entries")
    except Exception as e:
        print(f"Test 5 Failed: {e}")

    # Test 6: Boundary Values
    try:
        router_id = 1
        table = [[1024, 1, 64000], [64000, 15, 1024]]
        packet = rip_packet(router_id, table)
        print("Test 6 Passed: Boundary Values")
    except Exception as e:
        print(f"Test 6 Failed: {e}")

test_rip_packet()