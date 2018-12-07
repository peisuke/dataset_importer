# How to use

- JSON File (labels.json)
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
  "detection": [
    {
      "category_id": 0,
      "label_id": 1,
      "label": "Cat",
      "rect": {
        "ymax": 98.84285714285714,
        "xmax": 168.4908163265306,
        "ymin": 63.54183673469388,
        "xmin": 98.65204081632653
      }
    },
    {
      "category_id": 0,
      "label_id": 0,
      "label": "Dog",
      "rect": {
        "ymax": 58.96224489795919,
        "xmax": 80.52448979591837,
        "ymin": 2.0989795918367347,
        "xmin": 17.93673469387755
      }
    }
  ]
}
```
