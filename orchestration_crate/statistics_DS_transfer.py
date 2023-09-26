from gladier import GladierBaseTool


class statistics_DS_transfer(GladierBaseTool):


    flow_definition = {
        'Comment': 'Transfer results to datastore',
        'StartAt': 'statistics_DS_transfer',
        'States': {
            'statistics_DS_transfer': {
                'Comment': 'Transfer a directory to datastore',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.input.statistics_ep_id',
                    'destination_endpoint_id.$': '$.input.data_store_ep_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.input.statistics_path',
                            'destination_path.$': '$.input.datastore_path',
                            'recursive': True,
                        }
                    ]
                },
                'ResultPath': '$.statistics_DS_transfer',
                'WaitTime': 600,
                'End': True
            }
        }
    }


    funcx_functions = []
    
    flow_input = {
        'transfer_sync_level': 'checksum'
    }

    required_input = [
        'statistics_ep_id',
        'statistics_path',
        'data_store_ep_id',
        'data_store_path',
    ]

