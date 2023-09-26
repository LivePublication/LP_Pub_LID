from gladier import GladierBaseTool


class langdetect(GladierBaseTool):


    flow_definition = {
        'Comment': 'Executes langdetect classification on input_data.txt',
        'StartAt': 'langdetect',
        'States': {
            'langdetect': {
                'ActionScope': 'https://auth.globus.org/scopes/feda0005-01ad-414d-81ce-dcc5b7f61a1f/action_provider_operations',
                'ActionUrl': 'http://130.216.217.48:8080/langdetect',
                'Comment': 'Execute langdetect classification on input_data.txt',
                'Type': 'Action',
                'Parameters': {
                    'input_data.$': '$.input.langdetect_path',
                    'management_ep_id.$': '$.input.management_ep_id',
                },
                'End': True,
                'ResultPath': '$.langdetect',
                'WaitTime': 6000,
            },
        }
    }

    funcx_functions = []
    
    flow_input = {}

    required_input = [
        'langdetect_path',
        'management_ep_id',
    ]
