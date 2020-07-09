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
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from prettytable import PrettyTable
from azure import loganalytics



network_client = get_client_from_cli_profile(NetworkManagementClient)
ckt_count = 0
port_count = 0
port_table = PrettyTable()
port_table.field_names = ["ER Port", "Location", "Peering", "Prov BW", "Port BW", "Ckts", "Util"]
for port in network_client.express_route_ports.list():
    port_util = float(port.provisioned_bandwidth_in_gbps/port.bandwidth_in_gbps)
    if port.circuits:
        ckt_no = len(port.circuits)
    else:
        ckt_no = 0
    port_table.add_row([
        port.name, port.location, port.peering_location,
        port.provisioned_bandwidth_in_gbps,
        port.bandwidth_in_gbps, ckt_no,
        "{}%".format(port_util*100, 2)])
    ckt_count += ckt_no
    port_count += 1

print(port_table)
print("total ports provisioned = {}".format(port_count))
print("total circuits provisioned = {}".format(ckt_count))
