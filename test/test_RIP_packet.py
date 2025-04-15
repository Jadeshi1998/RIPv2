"""
用于在路由器之间传输路由信息,当一个路由器接收到RIP数据包时,它会解析数据包并根据其中的路由条目更新其路由表。
周期性更新: 30s.
当路由信息发生变化时(eg.，某条路由变得不可达），路由器会立即发送更新。
    Send to each neiboure for update the
    RIP Packet Structure 
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | command : 1/2   | version : 2  |      must be zero (2)       |
    +---------------+---------------+-------------------------------+
    |                  RIP Entry (20 bytes)                        |
    |                [(destination , metric),()...]                 |
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
    return header

def RIP_entry(table):
    # table = (destination:{ next_hop, cost, garbage flag})
    entry = []
    for destination, info in table.items():
        if info['garbage'] != True:  
    
            metric = info['cost']
            entry.append([destination, metric])
    return entry

def rip_packet(router_id, table):
    """Full RIP packet."""
    header = RIP_header(router_id)
    entries = RIP_entry(table)
    packet = {'header':header, 'entry':entries}
    return packet

def set_poisoned_reverse(router_ID, table, port_id):
    """Set poisoned reverse for routes learned from a specific neighbor."""
    poisoned_entries = []
    for destination, route_info in table.items():
        if (route_info['next_hop'] == port_id) and destination != port_id:
            # Set the metric to infinity for this route
            poisoned_entries.append((destination, 16))
        else:
            # Keep the original metric for other routes
            poisoned_entries.append((destination, route_info['cost']))
    # Construct the packet with the poisoned reverse entries
    poisoned_packet = {
        'header': RIP_header(router_ID),
        'entry': poisoned_entries
    }
    return poisoned_packet



def test_RIP_header():
    router_id = 1
    exp_header = [COMMAND_REQUEST, VERSION, router_id]
    header = RIP_header(router_id)
    assert header == exp_header
    print("test_RIP_header pass.")

def test_RIP_entry():
    table = {
        3: {'next_hop': 5, 'cost': 2, 'garbage': False},
        4: {'next_hop': 4, 'cost': 3, 'garbage': False},
        5: {'next_hop': 5, 'cost': 4, 'garbage': True}  # This entry should be ignored
    }
    exp_entries = [[3, 2], [4, 3]]
    entries = RIP_entry(table)
    assert entries == exp_entries
    print("test_RIP_entry pass.")

def test_rip_packet():
    router_id = 1
    table = {
        3: {'next_hop': 5, 'cost': 2, 'garbage': False},
        4: {'next_hop': 4, 'cost': 3, 'garbage': False}
    }
    exp_packet = {
        'header': [COMMAND_REQUEST, VERSION, router_id],
        'entry': [[3, 2], [4, 3]]
    }
    packet = rip_packet(router_id, table)
    assert packet == exp_packet
    print("test_rip_packet pass.")

def test_set_poisoned_reverse():
    #Send to router 5, with a router 3 use next hop 5, should set to 16
    router_ID = 1
    table = {
        3: {'next_hop': 5, 'cost': 2, 'garbage': False},
        4: {'next_hop': 4, 'cost': 3, 'garbage': False},
        5: {'next_hop': 5, 'cost': 4, 'garbage': False}
    }
    port_id = 5
    exp_packet = {
        'header': [COMMAND_REQUEST, VERSION, router_ID],
        'entry': [(3, 16), (4, 3), (5, 4)]
    }
    poisoned_packet = set_poisoned_reverse(router_ID, table, port_id)
    assert poisoned_packet == exp_packet
    print("test_set_poisoned_reverse pass.")


test_RIP_header()
test_RIP_entry()
test_rip_packet()
test_set_poisoned_reverse()