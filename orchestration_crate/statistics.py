from gladier import GladierBaseTool


class statistics(GladierBaseTool):

    flow_definition = {
        'Comment': 'Calculates accuracy statistics, and generates figures, tables, and objects to represent the results in the publication layer',
        'StartAt': 'statistics',
        'States': {
            'statistics': {
                'ActionScope': 'https://auth.globus.org/scopes/c45fe380-8e83-43da-a603-fffb0f4a782e/action_provider_operations',
                'ActionUrl': 'http://130.216.217.213:8080/statistics',
                'Comment': 'Calculates accuracy statistics, and generates figures, tables, and objects to represent the results in the publication layer',
                'Type': 'Action',
                'Parameters': {
                    'fastText_predictions.$': '$.input.fastText_predictions',
                    'langdetect_predictions.$': '$.input.langdetect_predictions',
                    'validation.$': '$.input.validation',
                    'management_ep_id.$': '$.input.management_ep_id',
                },
                'End': True,
                'ResultPath': '$.statistics',
                'WaitTime': 6000,
            },
        }
    }

    funcx_functions = []
    
    flow_input = {}

    required_input = [
        'fastText_predictions',
        'langdetect_predictions',
        'validation',
        'management_ep_id',
    ]
