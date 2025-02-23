


class config
"""
Reads configuration file
Returns a dictionary of routing table
Config Structure
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| router_id  | input_ports  |   output_ports  |  update_timers  |
+---------------+---------------+-------------------------------+
"""

def __init__(self):
        self.router_id = 0
        self.input_ports = []
        self.output_ports = []
        self.update_timers = 0

def parser_config(self,f):
    """
    Reads configuration file 
    Returns a dictionary of routing table
    """

    #Initialize the config structure
    config = {
        'router_id': None,
        'input_ports': [],
        'output_ports': [],
        'timers' : [],
    }

    #
    with open(f, 'r') as f:
        for line in f:
            #set a init timer 
            config['timers'] = [0, 0]

            line = line.strip()
            # Split line in dit structure content {key:value}
            # e.g. "router-id 1" ==> key:"router-id"; value:"1"
            parts = line.split(None, 1)
            #############################################
            if len(parts) != 2:
                raise ValueError(f"ERROR: Invalid line format: '{line}'")
            
            key, value = parts[0].lower(), parts[1].strip()
            #############################################
            if key == 'router-id':
                try:
                    in_ports = [int(p.strip()) for p in value.split(',')]
                    for port in in_ports:
                        if not (1024 <= port <= 64000):
                            raise ValueError(f"ERROR: Invalid input port {port}. Must be in range 1024-64000.")
                    config['input_ports'] = in_ports
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
                        peer_port_num = int(out[0])
                        metric = int(out[1])
                        peer_id = int(out[2])
                        if not (1024 <= peer_port_num <= 64000):
                            raise ValueError(f"ERROR: Invalid output port {peer_port_num}. Must be in range 1024-64000.")
                        out_ports.append((peer_port_num, metric, peer_id))
                    config['output_ports'] = out_ports
                except ValueError:
                    raise ValueError("ERROR: output_ports must be a comma-separated list of 'port-metric-peer_id'.")
        return config



            
class RIP_packet
command = '2'
version = '2'
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

def rip_header(config):
    """Build up rip packet header and  entry"""
    # rip packet header = [command, version, source]
    source = int(config['router_id'])
    header = [command, version, source]
    header_rep = f'{command},{version},{source}'
    print(f'RIP Header : command {command}, version {version}, source {source}')
    return header,header_rep
    
def rip_entry(config):
    # rip packet entry = metric + destination
    entry = []
    for destination in config.keys():
        metric = config[destination][0]
        entry.append((metric, destination)) 
    entry_rep = f''
    return entry

def rip_packet(header,entry):
    packet = {'header': header,
        'entry': entry,}  
    return packet

class routing_table
"""
Routing Table Structure
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Next Hop   |   Cost   |   Garbage(bool)     |     Dest.     |
+---------------+---------------+-------------------------------+
router ID , input ports , output ports, timers

Routing Table functions
set_timer/cost/garbage/next_hop
"""

class routing_daemon
"""
Routing Daemon Structure
"""

def server
"""
udp socket + bind
"""

