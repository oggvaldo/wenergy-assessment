# Azure Manager Functions

This Python script, `pytesting.py`, includes several functions designed to manage and interact with Azure resources. Below are the setup and execution instructions to effectively use this script.

## Prerequisites

- Python 3.x installed
- Azure CLI installed
- Active Azure subscription
- Appropriate permissions to manage resources in your Azure subscription

## Variables
Set the environment variables
export SUBSCRIPTION_ID="<INCLUDE THE AZURE SUBSCRIPTION>"
export PY_VM_USERNAME="pytest" 
export PY_VM_PASSWORD="<DEFINE A PASSWORD>" 
export PY_SQL_SERVER_PASSWORD="<DEFINE A PASSWORD>" 

## Setup

1. Install Required Python Packages
Install the necessary Python packages using pip:

pip install azure-identity azure-mgmt-compute azure-mgmt-network azure-mgmt-resource azure-mgmt-sql azure-mgmt-storage

This script assumes the use of the Azure SDK for Python, particularly modules for identity management and resource management. Adjust the installation command based on the actual dependencies used in the script.

2. Azure Authentication
Ensure that your Azure CLI is logged in to your Azure account:

az login

Follow the prompts to complete the authentication process.


## Running the Script

### Default Behavior
Run the script without arguments to create or upgrade the resources defined in the file:

python pytesting.py


### Script Arguments
You can pass arguments to the script for specific actions:

Start the VM created by the script:

python pytesting.py startvm


Stop the VM created by the script:

python pytesting.py stopvm


Delete the VM created by the script:

python pytesting.py deletevms


## Error Handling and Logging

### Error Handling
The pytesting.py script is designed to manage Azure resources robustly by incorporating comprehensive error handling to ensure reliability and maintainability. Here's how errors are handled:

Exception Catching: The script uses try-except blocks to catch and handle exceptions that may occur during the execution of Azure management tasks. This prevents the script from crashing and allows it to provide meaningful error messages.

Resource Validation: Before performing operations on Azure resources, the script validates the existence and state of these resources. If a required resource is not found or is in an incorrect state, the script logs an appropriate error and halts further execution.

Retry Logic: For operations that may fail due to temporary issues, such as network latency or rate limits, the script implements retry logic. It attempts to perform the operation multiple times (with a delay between retries) before finally logging an error if all attempts fail.


### Logging
Logging is an essential part of the pytesting.py script, providing insights into the operations performed and their outcomes. The script uses Python’s built-in logging module to log messages at various levels of severity. Here’s how logging is set up and used:

Log Configuration: The script configures logging at the beginning of execution, setting the log level and format. This typically includes the time, the level of severity, and the message.

Informational Logs: During normal operations, the script logs informational messages that detail the progress of the script, such as "Connecting to Azure...", "Successfully connected to Azure", "Starting VM creation...", etc.

Debug Logs: When debug mode is enabled, the script logs detailed information that can be used for troubleshooting or understanding the script’s behavior in depth.

Error Logs: Any errors encountered during the execution are logged at the error level. The log message includes the type of error and a message that describes what went wrong.

Critical Logs: For severe issues that may require immediate attention, such as failures in critical functions or data corruption, the script logs critical messages.
