"""
    信息的存储地在router内部储存记录了当前网络的拓扑结构和最佳路径。
    Routing Table Structure
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |     Dest(key)   |   Next Hop   |   Cost   |   Garbage(bool)    |
    +---------------+---------------+-------------------------------+
    router ID , input ports , output ports, timers

"""
METRIC_INFINITY = 16
routing_table = {}

def new_route(destination, next_hop, cost, garbage=False):
    """Add or update a route in the routing table."""
    if not (1 <= cost < METRIC_INFINITY):
        raise ValueError(f"ERROR: Invalid metric {cost}. Must be in range 1-15.")
    routing_table[destination] = {
        'next_hop': next_hop,
        'cost': cost,
        'garbage': garbage
    }
    print(f'Route added: {destination} -> Next Hop: {next_hop}, Cost: {cost}, Garbage: {garbage}')

def remove_route(destination):
    """Remove a route from the routing table."""
    if destination in routing_table:
        del routing_table[destination]
        print(f"Route removed: {destination}")

def flag_garbage(destination):
    """ Flag a route as garbage. """
    if destination in routing_table:
        routing_table[destination]['garbage'] = True
        print(f"Route marked as garbage: {destination}")

def print_table():
    """Print the current routing table."""
    print("Routing Table:")
    for dest, info in routing_table.items():
        print(f"Destination: {dest}, Next Hop: {info['next_hop']}, Cost: {info['cost']}, Garbage: {info['garbage']}")


def test_routing_table():
    #(destination, next_hop, cost,)
    new_route(2, 6, 1)
    new_route(3, 5, 2)
    new_route(4, 4, 3)
    print_table()
    flag_garbage(3)
    print_table()
    remove_route(2)
    print_table()

test_routing_table()
