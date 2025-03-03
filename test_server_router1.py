import Server as s
import config as cfg
config_filename = 'router1.txt'
table = cfg.read_config(config_filename)
input_ports = table['input_ports']
print(f"Input_ports : {input_ports}")
neighbor_port = [i[0] for i in table['output_ports']]

print(f"Neighbor ports : {neighbor_port}")
s.server(input_ports, neighbor_port)