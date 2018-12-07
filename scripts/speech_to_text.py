import json
import os
import argparse

import abeja
from abeja.datasets import APIClient

from abejacli.config import (
    ABEJA_PLATFORM_USER_ID, ABEJA_PLATFORM_TOKEN
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotation Data Importer: Speech to text')
    parser.add_argument('--input', '-i', required=True, help='Annotated data from Annotation Tool')
    parser.add_argument('--organization', '-o', required=True, help='Organization ID')
    parser.add_argument('--dataset', '-d', required=True, help='Output Dataset Name')
    args = parser.parse_args()

    credential = {
        'user_id': ABEJA_PLATFORM_USER_ID,
        'personal_access_token': ABEJA_PLATFORM_TOKEN
    }
    
    organization_id = args.organization
    datasetname = args.dataset

    with open(args.input, 'r') as f:
        data = json.load(f)

    category = {
        'labels': [],
        'category_id': 0,
        'name': datasetname
    }
    props = {'categories': [category]}

    api_client = APIClient(credential)
    dataset = api_client.create_dataset(organization_id, datasetname, 'custom', props)

    dataset_id = dataset['dataset_id']

    for d in data:
        channel_id = d['task']['metadata'][0]['channel_id']
        
        info = []
        for t in d['information']:        
            info.append({'category_id': 0, 'text': t['text']})
        filename = d['task']['metadata'][0]['information']['filename']
        file_id = d['task']['metadata'][0]['source']
    
        if os.path.splitext(filename)[1].lower() == '.mp3':
            content_type = 'audio/mp3'
        else:
            print('{} is invalid file type.'.format(filename))
            continue
    
        data_uri = 'datalake://{}/{}'.format(channel_id, file_id)
        source_data = [{'data_uri': data_uri, 'data_type': content_type}]
        attributes = {'image_to_text': info}
    
        api_client.create_dataset_item(organization_id, dataset_id, source_data, attributes)
