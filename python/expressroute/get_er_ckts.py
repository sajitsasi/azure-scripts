#!/usr/bin/env python3
############################################################################
# This is demo code and not intended for use in production.  As such this
# code demonstrates how to get query azure circuits and gather bandwidth
# utilization for said circuit.
#
# USE AT YOUR OWN RISK!!!
#
# Author: Sajit Sasi
# Author Email: sajit.sasi@microsoft.com
############################################################################

from azure.common.client_factory import get_client_from_cli_profile
from azure.common.client_factory import get_azure_cli_credentials
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from prettytable import PrettyTable
from azure import loganalytics
import os, sys



network_client = get_client_from_cli_profile(NetworkManagementClient)
log_cred, _ = get_azure_cli_credentials(resource="https://api.loganalytics.io")
la_client = loganalytics.log_analytics_data_client.LogAnalyticsDataClient(log_cred)

if 'LA_WORKSPACE_ID' in os.environ:
    workspace_id = os.environ['LA_WORKSPACE_ID']
else:
    print("LA_WORKSPACE_ID environment variable not defined!!!")
    sys.exit(-1)

count = 0
er_ports = {}
ckt_table = PrettyTable()
ckt_table.field_names = ["Time", "ER Ckt", "Tenant", "In(Gbps)", "Out(Gbps)", "Total(Gbps)", "Prov BW(Gbps)", "BW Util"]
for ckt in network_client.express_route_circuits.list_all():
    query = 'AzureMetrics | where ResourceId contains "{}" | where MetricName == "BitsInPerSecond" | where TimeGenerated > (now() - 15m) and TimeGenerated <= now() | project TimeGenerated, Resource, inBytes=Average | join kind= inner ( AzureMetrics | where MetricName == "BitsOutPerSecond" | where TimeGenerated > (now() - 15m) and TimeGenerated <= now() | project TimeGenerated, Resource, outBytes=Average) on TimeGenerated, Resource | summarize data_in = avg(inBytes), data_out = avg(outBytes), data_total = sum(inBytes + outBytes) by bin(TimeGenerated, 1m), Resource | order by TimeGenerated'.format(ckt.name.upper())

    body = loganalytics.models.QueryBody(query=query)
    query_results = la_client.query(workspace_id, body)
    rows = 0
    if query_results.tables[0].rows:
        row = query_results.tables[0].rows[0]
    else:
        row = None
    if row and row[4] != 0: 
        tenant = 'N/A'
        if ckt.tags and 'Tenant' in ckt.tags:
            tenant = ckt.tags['Tenant']
        bw_util = round(((row[4]/1000000000.0)/ckt.bandwidth_in_gbps)*100, 2)
        ckt_table.add_row([
            row[0], row[1], tenant, round(row[2]/1000000000.0,2),
            round(row[3]/1000000000.0,4), round(row[4]/1000000000.0,4), 
            ckt.bandwidth_in_gbps, "{}%".format(bw_util)])
print(ckt_table)
