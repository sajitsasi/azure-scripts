#!/usr/bin/env python3

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
An example to show receiving events from an Event Hub.
"""
import os
import json
from azure.eventhub import EventHubConsumerClient


def update_seq_file(seq_number):
    if not (seq_number or isinstance(seq_number, int)):
        return
    fd = open(".seq", "w")
    fd.write(f"{seq_number}")
    fd.flush()
    fd.close()

def on_event(partition_context, event):
    # Put your code here.
    # If the operation is i/o intensive, multi-thread will have better performance.
    print("Received event from partition: {}.".format(
        partition_context.partition_id))
    for val in event.body:
        if isinstance(val, bytes):
            print(val.decode("utf-8"))
    update_seq_file(int(event.sequence_number))
    return
#    event_data = event.body_as_json()
#    print(json.dumps(event_data, indent=2))


def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(partition_context.partition_id))


def on_partition_close(partition_context, reason):
    # Put your code here.
    print("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def main():
    CONNECTION_STR = os.environ["EVENT_HUBS_CONN_STR"]
    EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']
    CONSUMER_GROUP = os.environ['CONSUMER_GROUP']
    seq_file = ".seq"
    global g_sequence_number
    initial_seq = -1

    if os.path.isfile(seq_file):
        fd = open(seq_file, 'r')
        for line in fd:
            initial_seq = int(line.strip())
            break
        fd.close()
    else:
        initial_seq = -1

    print("initial seq is {}".format(initial_seq))
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENTHUB_NAME,
    )
    try:
        with consumer_client:
            consumer_client.receive(
                on_event=on_event,
                on_partition_initialize=on_partition_initialize,
                on_partition_close=on_partition_close,
                on_error=on_error,
                starting_position=initial_seq,  # "-1" is from the beginning of the partition.
            )
    except KeyboardInterrupt:
        print('Stopped receiving.')


if __name__ == '__main__':
    main()

