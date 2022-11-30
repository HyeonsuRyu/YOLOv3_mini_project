"""
make label in format below:
[
    {
        "name": "image_name",
        "labels": [
            {
                "id": "label_id",
                "category": "label_category",
                "attributes": {
                    "crowd": false,
                    "occluded": false,
                    "truncated": false,
                }
                "box2d": {
                    "x1": 0.0,
                    "x2": 0.0,
                    "y1": 0.0,
                    "y2": 0.0,
                }
            }
            . . .
        ]
    }
]

this format should be changed to fit in the model
"""

# not implemented