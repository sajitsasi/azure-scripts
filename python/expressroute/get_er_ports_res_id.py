#!/usr/bin/env python3
############################################################################
# This is demo code and not intended for use in production.  As such this
# code demonstrates how to get query azure ER Direct ports and gather
# utilization for said ports.
#
# USE AT YOUR OWN RISK!!!
#
# Author: Sajit Sasi
# Author Email: sajit.sasi@microsoft.com
############################################################################


from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.network import NetworkManagementClient
from prettytable import PrettyTable



network_client = get_client_from_cli_profile(NetworkManagementClient)
ckt_count = 0
port_count = 0
port_table = PrettyTable()
port_table.field_names = ["ER Port", "Resource ID"]
for port in network_client.express_route_ports.list():
    port_table.add_row([port.name, port.id]) 

print(port_table)
