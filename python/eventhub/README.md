# azure-scripts/python/eventhub

This repository contains a sample set of scripts that I use for 
[Azure Event Hubs](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-about)

NOTE: This is for demo purposes only and should not be used for production
code except as a starting point

## Assumptions
1. You have already created an [Event Hubs Namespace and event hub](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-quickstart-cli)

## Instructions
1. Download the git repo to your directory:
   ```
   git clone https://github.com/sajitsasi/azure-scripts.git
   cd azure-scripts/python/eventhub
   ```
2. Modify `sample_env` with correct values:
   ```
   EVENT_HUBS_NAMESPACE="your_event_hubs_namespace_name_without_FQDN"
   EVENT_HUBS_POLICY="your_SAS_POLICY"
   EVENT_HUBS_KEY="your_SAS_Key"
   EVENT_HUBS_CONN_STR="your_SAS_Connection_String"
   EVENT_HUB_NAME="event_hub_name"
   CONSUMER_GROUP="<Consumer Group default value is '\$Default'>"
   ```
3. Source the environment file `. ./sample_env`
4. Start listening for events by typing `./consumer_amqp.py`
5. Open another terminal, and run Step 3 above to source environment and start sending events with `./producer_amqp.py` or `./producer_https.py`

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
