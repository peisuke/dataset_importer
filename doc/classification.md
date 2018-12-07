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

- Attributes
```
{
  "classification": [
    {
      "category_id": 0,
      "label_id": 0,
      "label": "Dog"
    }
  ]
}
```
