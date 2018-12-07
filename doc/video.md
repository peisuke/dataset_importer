# How to use

- JSONデータ
```
[
  {
    "label_id": 0,
    "label": "Dog"
  },
  {
    "label_id": 1,
    "label": "Cat"
  }
]
```

# Format

- Data source
```
[
  {
    "data_uri": "datalake://{CHANNEL_ID}/{FILE_ID}",
    "data_type": "image/jpeg"
  }
]
```

```
{
  "video": [
    {
      "starting_frames_count": 0,
      "label": "Dog",
      "end": 1.67333,
      "label_id": 0,
      "start": 0,
      "ending_frames_count": 50.1999,
      "category_id": 0
    },
    {
      "starting_frames_count": 52.244910000000004,
      "label": "Dog",
      "end": 3.105347,
      "label_id": 0,
      "start": 1.741497,
      "ending_frames_count": 93.16041,
      "category_id": 0
    },
    {
      "starting_frames_count": 95.43402,
      "label": "Cat",
      "end": 4.299703,
      "label_id": 1,
      "start": 3.181134,
      "ending_frames_count": 128.99109,
      "category_id": 0
    }
  ]
}
```
