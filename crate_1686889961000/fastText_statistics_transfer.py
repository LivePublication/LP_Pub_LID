from gladier import GladierBaseTool


class fastText_statistics_transfer(GladierBaseTool):


    flow_definition = {
        'Comment': 'Transfer the prefix_list from i_1 to c_1 for processing',
        'StartAt': 'fastText_statistics_transfer',
        'States': {
            'fastText_statistics_transfer': {
                'Comment': 'Transfer a file or directory in Globus',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.input.fastText_ep_id',
                    'destination_endpoint_id.$': '$.input.statistics_ep_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.input.fastText_path',
                            'destination_path.$': '$.input.statistics_path',
                            'recursive': False,
                        }
                    ]
                },
                'ResultPath': '$.fastText_statistics_transfer',
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
        'fastText_ep_id',
        'fastText_path',
        'statistics_ep_id',
        'statistics_path',
    ]

