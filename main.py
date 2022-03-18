import json, importlib


# Simulating main proccess 
# this will work forever and pull all new tasks
def run_tasks():

    # crawler deffinitions to call different class for diffrent tasks.
    crawlers = {
        'MOCK_INDEMNITY':{
            "name": "MockIndemnity",
            "path": "crawlers.mock_indemnity"
        },
        'PLACEHOLDER_CARRIER':{
            "name": "PlaceholderCarrier",
            "path": "crawlers.placeholder_carrier"
        },

    }

    with open('task_list_queue.json') as tasks_file:
        tasks = json.load(tasks_file)
        for task in tasks:
            if task['carrier'] in crawlers:
                # Get Module
                m = crawlers[task['carrier']]

                # Import python Module dynamicly
                module = importlib.import_module(m['path'])

                # get Class from module
                my_class = getattr(module, m['name'])
                
                # Create Class instance
                my_instance = my_class(task['customerId'])

                # start Crawler
                my_instance.run()
            else: 
                print('Crawler not found...')


if(__name__ == "__main__"):
    run_tasks()