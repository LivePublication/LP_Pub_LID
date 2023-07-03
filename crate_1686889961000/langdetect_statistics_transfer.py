from gladier import GladierBaseTool


class langdetect_statistics_transfer(GladierBaseTool):


    flow_definition = {
        'Comment': 'Transfer the prefix_list from i_1 to c_1 for processing',
        'StartAt': 'langdetect_statistics_transfer',
        'States': {
            'langdetect_statistics_transfer': {
                'Comment': 'Transfer a file or directory in Globus',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.input.langdetect_ep_id',
                    'destination_endpoint_id.$': '$.input.statistics_ep_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.input.langdetect_path',
                            'destination_path.$': '$.input.statistics_path',
                            'recursive': False,
                        }
                    ]
                },
                'ResultPath': '$.langdetect_statistics_transfer',
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
        'langdetect_ep_id',
        'langdetect_path',
        'statistics_ep_id',
        'statistics_path',
    ]

