from gladier import GladierBaseTool


class DS_langDetect_transfer(GladierBaseTool):


    flow_definition = {
        'Comment': 'Transfer the prefix_list from i_1 to c_1 for processing',
        'StartAt': 'DS_langDetect_transfer',
        'States': {
            'DS_langDetect_transfer': {
                'Comment': 'Transfer a file or directory in Globus',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.input.data_store_ep_id',
                    'destination_endpoint_id.$': '$.input.langDetect_ep_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.input.data_store_path',
                            'destination_path.$': '$.input.langDetect_path',
                            'recursive': False,
                        }
                    ]
                },
                'ResultPath': '$.DS_langDetect_transfer',
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
        'langDetect_ep_id',
        'langDetect_path',
    ]

