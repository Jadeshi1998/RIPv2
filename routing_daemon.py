# Description: This file contains the routing daemon implementation

class config:
    """
    Reads configuration file
    Returns a dictionary of routing table
    Config Structure
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | router_id  | input_ports  |   output_ports  |  update_timers  |
    +------------+--------------+-----------------+-----------------+
    """

    def __init__(self):
            self.router_id = None
            self.input_ports = []
            #output_ports = [(port, cost,router_id), ()...]
            self.output_ports = [0,0,0]
            self.update_timers = []

    def __str__(self):
        return f'Config id={self.router_id}, input_ports={self.input_ports}, output_ports={self.output_ports}, periodic_update={self.update_timers:.4}s'

    def __repr__(self):
        return self.__str__()
    


def parser_config(f):
    """
    Reads configuration file 
    +++++++++++++++++++++++++++++++++++++++++
    router-id 1
    input-ports 6110, 6201, 7345
    outputs 5000-1-1, 5002-5-4
    +++++++++++++++++++++++++++++++++++++++++
    """
    config = {
        'router_id': None,
        'input_ports': [],
        'output_ports': [0,0,0],
        'timers' : [],
    }

    #set a init timer 
    config.update_timers = [0, 0]
    with open(f, 'r') as f:
        for line in f:
            line = line.strip()
            # Split line in dit structure content {key:value}
            # e.g. "router-id 1" ==> key:"router-id"; value:"1"
            parts = line.split(None, 1)
            #############################################
            if len(parts) != 2:
                raise ValueError(f'ERROR: Invalid line format: {line}')
            
            key, value = parts[0].lower(), parts[1].strip()
            #############################################
            if key == 'router-id':
                try:
                    in_ports = [int(p.strip()) for p in value.split(',')]
                    #check in_ports
                    for port in in_ports:
                        if not (1024 <= port <= 64000):
                            raise ValueError(f"ERROR: Invalid input port {port}. Must be in range 1024-64000.")
                    input_ports = in_ports
                except ValueError:
                    raise ValueError("ERROR: input_ports must be a comma-separated list of integers.")
            
            #############################################
            elif key == 'output-ports':
                try:
                    out_ports = []
                    for out in value.split(','):
                        out_parts = out.strip().split('-')
                        if len(out_parts) != 3:
                            raise ValueError(f"ERROR: Invalid output-port format")
                        #out_ports(port, cost,router_id)
                        peer_port_num = int(out[0])
                        metric = int(out[1])
                        peer_id = int(out[2])
                        if not (1024 <= peer_port_num <= 64000):
                            raise ValueError(f"ERROR: Invalid output port {peer_port_num}. Must be in range 1024-64000.")
                        out_ports.append((peer_port_num, metric, peer_id))
                    output_ports = out_ports
                except ValueError:
                    raise ValueError("ERROR: output_ports must be a comma-separated list of 'port-metric-peer_id'.")
        return config  


            
class RIP_packet:
    """
    RIP Packet Structure

        0                   1                   2                   3  
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1  
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | command (1)   | version (1)   |       must be zero (2)       |
    +---------------+---------------+-------------------------------+
    |                  RIP Entry (20 bytes)                        |
    |                 (May repeat multiple times)                  |
    +---------------------------------------------------------------+
    """
    command = 2
    version = 2
    def __init__(self):
        self.command = 2
        self.version = 2
        self.source = 0
        #entry = [(metric, destination),()...]
        self.entry = ''
    
    def __str__(self):
        return f'command : {self.command}, version : {self.version}, source : {self.source}, entry : {self.entry}'
    
    def __repr__(self):
        return self.__str__()

    def rip_header(config):
    """Build up rip packet header and entry"""
    # rip packet header = [command, version, source]
        source = int(config['router_id'])
        header = [command, version, source]
        return header,header_rep
    
    def rip_entry(config):
    # rip packet entry = metric + destination
        entry = []
        for destination in config.keys():
            metric = config[destination][0]
            entry.append((metric, destination)) 
        return entry


class routing_table:
    """
    Routing Table Structure
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Next Hop   |   Cost   |   Garbage(bool)     |     Dest.     |
    +---------------+---------------+-------------------------------+
    router ID , input ports , output ports, timers

    Routing Table functions
    set_timer/cost/garbage/next_hop
    """
    def __init__(self):
            self.next_hop = 0
            self.total_cost = []
            self.garbage = []
            self.dest = 0


class routing_daemon:
"""
Routing Daemon Structure
"""

def server
"""
udp socket + bind

"""

