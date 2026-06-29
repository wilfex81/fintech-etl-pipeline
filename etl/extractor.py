import json

#Load JSON file

def extract_payload(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Iterate over each record and parse the Payload field
    for record in data:
        record['Payload'] = json.loads((record['Payload']))

    return data