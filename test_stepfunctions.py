import json
import time
from assertpy import assert_that
from conftest import get_mock_table, mock_stepfunctions, TABLE_NAME, mock_stepfunctions_statemachine

ITEM_ID = "TEST_ITEM_ID"

def test_stepfunctions_stores_item(get_mock_table, mock_stepfunctions, mock_stepfunctions_statemachine):
    kwargs = {
        'stateMachineArn': mock_stepfunctions_statemachine['stateMachineArn'],
        'name': 'test_store_offer_object_run',
        'input': json.dumps({
            'item': {
                'item_id': ITEM_ID,
                'item_status': 'new item'
            }
        })
    }
    response = mock_stepfunctions.start_execution(**kwargs)
    execution_arn = response['executionArn']

    execution_description = mock_stepfunctions.describe_execution(executionArn=execution_arn)

    while(execution_description['status'] == 'RUNNING'):
        execution_description = mock_stepfunctions.describe_execution(executionArn=execution_arn)

    assert_that(execution_description['status']).is_equal_to('SUCCEEDED')

    scan_result = get_mock_table.scan(TableName=TABLE_NAME)
    assert_that(scan_result['Items']).is_length(1)
    assert_that(scan_result['Items'][0]['item_status']).is_equal_to('updated')
    assert_that(scan_result['Items'][0]['item_id']).is_equal_to(ITEM_ID)