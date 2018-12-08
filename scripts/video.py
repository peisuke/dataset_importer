import json
import os
import argparse

import abeja
from abeja.datasets import APIClient

from abejacli.config import (
    ABEJA_PLATFORM_USER_ID, ABEJA_PLATFORM_TOKEN
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotation Data Importer: Video')
    parser.add_argument('--input', '-i', required=True, help='Annotated data from Annotation Tool')
    parser.add_argument('--organization', '-o', required=True, help='Organization ID')
    parser.add_argument('--attributes', '-a', default='attributes/attributes_classification.json', help='Attributes file')
    parser.add_argument('--dataset', '-d', required=True, help='Output Dataset Name')
    args = parser.parse_args()

    credential = {
        'user_id': ABEJA_PLATFORM_USER_ID,
        'personal_access_token': ABEJA_PLATFORM_TOKEN
    }
    
    organization_id = args.organization
    datasetname = args.dataset

    with open(args.attributes, 'r') as f:
        attributes = json.load(f)
   
    categories = attributes['attributes']
   
    labels =[]
    label_to_id = {}
    for count, cat in enumerate(categories):
        label_to_id[cat['name']] = count
        labels.append({
            'label': cat['name'],
            'label_id': count
        })

    with open(args.input, 'r') as f:
        data = json.load(f)

    category = {
        'labels': labels,
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
        for pos in d['information']:  
            start = pos['start']
            end = pos['end']
            sfc = pos['starting_frames_count']
            efc = pos['ending_frames_count']
            label = pos['category_name']
            label_id = label_to_id[label]
            info.append({
                'start': start,
                'end': end,
                'starting_frames_count': sfc,
                'ending_frames_count': efc,
                'label': label,
                'label_id': label_id,
                'category_id': 0,
            })

        filename = d['task']['metadata'][0]['information']['filename']
        file_id = d['task']['metadata'][0]['source']

        if os.path.splitext(filename)[1].lower() == '.mp4':
            content_type = 'video/mp4'
        else:
            print('{} is invalid file type.'.format(filename))
            continue

        data_uri = 'datalake://{}/{}'.format(channel_id, file_id)
        source_data = [{'data_uri': data_uri, 'data_type': content_type}]
        attributes = {'video': info}

        api_client.create_dataset_item(organization_id, dataset_id, source_data, attributes)
