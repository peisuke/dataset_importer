import io
import argparse
from PIL import Image
from abeja.datasets import Client
from abeja.datalake import APIClient as DatalakeClient
from abeja.datalake.file import DatalakeFile

from abejacli.config import (
    ABEJA_PLATFORM_USER_ID, ABEJA_PLATFORM_TOKEN
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DataSet Viewer: Segmentation')
    parser.add_argument('--organization', '-o', required=True, help='Organization ID')
    parser.add_argument('--dataset', '-d', required=True, help='Dataset ID')
    args = parser.parse_args()

    credential = {
        'user_id': ABEJA_PLATFORM_USER_ID,
        'personal_access_token': ABEJA_PLATFORM_TOKEN
    }

    client = Client(organization_id=args.organization, credential=credential)
    datalake_client = DatalakeClient(credential=credential)
    dataset = client.get_dataset(args.dataset)

    dataset_list = dataset.dataset_items.list(prefetch=False)

    for d in dataset_list:
        break

    file_content = d.source_data[0].get_content()
    file_like_object = io.BytesIO(file_content)
    
    img = Image.open(file_like_object)
    img.show()

    uri = d.attributes['segmentation'][0]['uri']
    ftype = 'image/png'
    datalake_file = DatalakeFile(datalake_client, args.organization, uri=uri, type=ftype)

    file_content = datalake_file.get_content()
    file_like_object = io.BytesIO(file_content)
    
    img = Image.open(file_like_object)
    img.show()
