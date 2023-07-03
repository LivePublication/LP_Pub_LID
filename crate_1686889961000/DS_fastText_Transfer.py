from gladier import GladierBaseTool


class DS_fastText_Transfer(GladierBaseTool):


    flow_definition = {
        'Comment': 'Transfer the prefix_list from i_1 to c_1 for processing',
        'StartAt': 'DS_fastText_Transfer',
        'States': {
            'DS_fastText_Transfer': {
                'Comment': 'Transfer a file or directory in Globus',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.input.data_store_ep_id',
                    'destination_endpoint_id.$': '$.input.fastText_ep_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.input.data_store_path',
                            'destination_path.$': '$.input.fastText_path',
                            'recursive': False,
                        }
                    ]
                },
                'ResultPath': '$.DS_fastText_Transfer',
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
        'data_store_ep_id',
        'data_store_path',
        'fastText_ep_id',
        'fastText_path',
    ]

