import io
import argparse
import cv2
from abeja.datasets import Client

from abejacli.config import (
    ABEJA_PLATFORM_USER_ID, ABEJA_PLATFORM_TOKEN
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DataSet Viewer: Video')
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

    with open('tmp.mp4', 'wb') as f:
        f.write(file_content)

    cap = cv2.VideoCapture('tmp.mp4')
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imshow('video', frame)
        cv2.waitKey(1)
