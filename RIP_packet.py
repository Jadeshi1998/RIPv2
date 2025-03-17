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
            #if destination != poisoned_route:
            metric = info['cost']
            entry.append([destination, metric])
            #print(f'Destination: {destination}, Cost: {metric}')
    return entry

def rip_packet(router_id, table):
    """Full RIP packet."""
    header = RIP_header(router_id)
    entries = RIP_entry(table)
    packet = {'header':header, 'entry':entries}
    return packet

def set_poisoned_reverse(router_ID, table, neighbor_ID):
    """Set poisoned reverse for routes learned from a specific neighbor."""
    poisoned_entries = []
    for destination, route_info in table.items():
        # Check if the route was learned from the neighbor
        if route_info['next_hop'] == neighbor_ID:
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

#router_id = 1
#table = {3: {'next_hop': 5, 'cost': 2, 'garbage': False}, 4: {'next_hop': 4, 'cost': 3, 'garbage': False}} # (destination:{next_hop, cost ,garbage flag})
#packet = rip_packet(router_id, table)
#print(packet)
#{'header': [1, 2, 1], 'entry': [[3, 2], [4, 3]]}