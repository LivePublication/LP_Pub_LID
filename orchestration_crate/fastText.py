from gladier import GladierBaseTool


class fastText(GladierBaseTool):


    flow_definition = {
        'Comment': 'Executes fastText classification on input_data.txt using fastText LiD model',
        'StartAt': 'fastText',
        'States': {
            'fastText': {
                'ActionScope': 'https://auth.globus.org/scopes/ca022ddb-b17d-4004-b600-4f15354a297c/action_provider_operations',
                'ActionUrl': 'http://130.216.216.5:8080/fastText',
                'Comment': 'Execute fastText classification on input_data.txt',
                'Type': 'Action',
                'Parameters': {
                    'input_data.$': '$.input.fastText_path',
                    'management_ep_id.$': '$.input.management_ep_id',
                },
                'End': True,
                'ResultPath': '$.fastText',
                'WaitTime': 6000,
            },
        }
    }

    funcx_functions = []
    
    flow_input = {}

    required_input = [
        'fastText_path',
        'management_ep_id',
    ]
