import json
import os
import argparse

import abeja
from abeja.datasets import APIClient

from abejacli.config import (
    ABEJA_PLATFORM_USER_ID, ABEJA_PLATFORM_TOKEN
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotation Data Importer: Segmentation')
    parser.add_argument('--input', '-i', required=True, help='Annotated data from Annotation Tool')
    parser.add_argument('--organization', '-o', required=True, help='Organization ID')
    parser.add_argument('--label', '-l', default='data/labels.json', help='Label JSON file')
    parser.add_argument('--dataset', '-d', required=True, help='Output Dataset Name')
    args = parser.parse_args()

    credential = {
        'user_id': ABEJA_PLATFORM_USER_ID,
        'personal_access_token': ABEJA_PLATFORM_TOKEN
    }
    
    organization_id = args.organization
    datasetname = args.dataset

    with open(args.label, 'r') as f:
        labels = json.load(f)
    
    with open(args.input, 'r') as f:
        data = json.load(f)

    category = {
        'labels': labels,
        'category_id': 0,
        'name': datasetname
    }
    props = {'categories': [category]}

    api_client = APIClient(credential)
    dataset = api_client.create_dataset(organization_id, datasetname, 'segmentation', props)

    dataset_id = dataset['dataset_id']

    label_to_id = {}
    for lbl in labels:
        label_to_id[lbl['label']] = lbl['label_id']

    for d in data:
        channel_id = d['task']['metadata'][0]['channel_id']
    
        info = {}
        for seg in data[0]['information']:
            if 'is_combined' in seg and seg['is_combined'] is True:
                info['category_id'] = 0
                cid = d['result_data_lake_channel']['channel_id']
                fid = seg['file_id']
                seg_uri = 'datalake://{}/{}'.format(cid, fid)
                info['uri'] = seg_uri
            
        filename = d['task']['metadata'][0]['information']['filename']
        file_id = d['task']['metadata'][0]['source']
    
        if os.path.splitext(filename)[1].lower() == '.jpg' or \
           os.path.splitext(filename)[1].lower() == '.jpeg':
            content_type = 'image/jpeg'
        elif os.path.splitext(filename)[1].lower() == '.png':
            content_type = 'image/png'
        else:
            print('{} is invalid file type.'.format(filename))
            continue
    
        data_uri = 'datalake://{}/{}'.format(channel_id, file_id)
        source_data = [{'data_uri': data_uri, 'data_type': content_type}]
        attributes = {'segmentation': [info]}
    
        api_client.create_dataset_item(organization_id, dataset_id, source_data, attributes)