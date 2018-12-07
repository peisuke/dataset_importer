import io
import argparse
from PIL import Image
from abeja.datasets import Client

from abejacli.config import (
    ABEJA_PLATFORM_USER_ID, ABEJA_PLATFORM_TOKEN
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DataSet Viewer: Classification')
    parser.add_argument('--organization', '-o', required=True, help='Organization ID')
    parser.add_argument('--dataset', '-d', required=True, help='Dataset ID')
    args = parser.parse_args()

    credential = {
        'user_id': ABEJA_PLATFORM_USER_ID,
        'personal_access_token': ABEJA_PLATFORM_TOKEN
    }

    client = Client(organization_id=args.organization, credential=credential)
    dataset = client.get_dataset(args.dataset)

    dataset_list = dataset.dataset_items.list(prefetch=False)

    for d in dataset_list:
        break

    print(d.attributes)
    
    file_content = d.source_data[0].get_content()
    file_like_object = io.BytesIO(file_content)
    
    img = Image.open(file_like_object)
    img.show()
