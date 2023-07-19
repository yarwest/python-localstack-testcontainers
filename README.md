# Python Localstack TestContainers Demo

This repository contains an example of testing an AWS Step Functions state machine using Python Testcontainers, LocalStack and Boto3. LocalStack is used to create a local deployment of the state machine, which runs inside a Docker container. This state machine can then be executed and any functionality (such as storing items in DynamoDB) can then be verified.

In this example a state machine has been defined (see `statemachine.json`), which stores and updates an item in a DynamoDB table. Inside `conftest.py` a LocalStack environment is initialized, in which a Step Functions state machine and DynamoDB table are created through Boto3. The actual test case can be found in `test_stepfunctions.py`, in which we execute the state machine and validate that the item has successfully been stored and update inside the DynamoDB table.

## Getting started

This sample code requires a Docker client to be able to execute the test case.

It is a good practice to logically seperate your Python projects through the use of virtual environments, this ensures that only the packages that are explicitely installed in this specific environment will be available. To manually create a virtual environment on MacOS and Linux you can use the following command line command:

`$ python3 -m venv .venv`

After the initialization process completes and the virtualenv is created, you can use the following command to activate your virtualenv and start using it:

`$ source .venv/bin/activate`

If you are using a Windows platform, you need to activate the virtualenv like this:

`% .venv\Scripts\activate.bat`

After activating the virtual environment, the required dependencies (see `requirements.txt`) need to be installed, this can be done using pip:

`pip3 install -r requirements.txt`

After succesfully fulfilling the dependencies, the test case can simply be executed using the `pytest` command.