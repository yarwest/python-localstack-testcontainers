import os
import boto3
import pytest

from testcontainers.localstack import LocalStackContainer

TABLE_NAME = "MOCK_TABLE_NAME"
STEPFUNCTION_NAME = "MOCK_STEPFUNCTION"

def get_resource_path(relative_path: str):
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, relative_path)


@pytest.fixture(autouse=True)
def create_localstack():
    localstack = LocalStackContainer(
        image='localstack/localstack:1.3.1').with_services("dynamodb", "stepfunctions")
    localstack.start()
    global localstack_endpoint
    localstack_endpoint = localstack.get_url()
    yield localstack
    localstack.stop()


@pytest.fixture
def mock_dynamodb():
    yield boto3.resource("dynamodb", endpoint_url=localstack_endpoint)


@pytest.fixture(autouse=True)
def mock_table(mock_dynamodb):
    table = mock_dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "item_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "item_id", "AttributeType": "S"}
        ],
        BillingMode="PROVISIONED",
        ProvisionedThroughput={
            'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
    )
    table.wait_until_exists()
    yield table


@pytest.fixture
def get_mock_table(mock_dynamodb):
    yield mock_dynamodb.Table(TABLE_NAME)


@pytest.fixture
def mock_stepfunctions():
    yield boto3.client("stepfunctions", endpoint_url=localstack_endpoint)


@pytest.fixture
def mock_stepfunctions_statemachine(mock_stepfunctions):
    with open(get_resource_path("statemachine.json"), 'r') as offer_statemachine:
        statemachine_str = offer_statemachine.read()
        statemachine_str = statemachine_str.replace('${mock_dynamodb_table_name}', TABLE_NAME)
        statemachine = mock_stepfunctions.create_state_machine(
            name=STEPFUNCTION_NAME,
            definition=statemachine_str,
            roleArn='arn:aws:iam::012345678901:role/DummyRole'
        )
        yield statemachine
