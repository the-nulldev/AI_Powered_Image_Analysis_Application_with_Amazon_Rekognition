"""
Please provide the JSON reply you received from the command between the triple quotes below.
Do not change the variable name or the triple quotes surrounding the JSON reply.
"""
labels_json = """
{
    "Labels": [
        {
            "Name": "Food",
            "Confidence": 99.82061767578125,
            "Instances": [],
            "Parents": [],
            "Aliases": [],
            "Categories": [
                {
                    "Name": "Food and Beverage"
                }
            ]
        },
        {
            "Name": "Plant",
            "Confidence": 99.82061767578125,
            "Instances": [],
            "Parents": [],
            "Aliases": [],
            "Categories": [
                {
                    "Name": "Plants and Flowers"
                }
            ]
        },
        {
            "Name": "Produce",
            "Confidence": 99.82061767578125,
            "Instances": [],
            "Parents": [
                {
                    "Name": "Food"
                }
            ],
            "Aliases": [],
            "Categories": [
                {
                    "Name": "Food and Beverage"
                }
            ]
        },
        {
            "Name": "Tomato",
            "Confidence": 99.82061767578125,
            "Instances": [],
            "Parents": [
                {
                    "Name": "Food"
                },
                {
                    "Name": "Plant"
                },
                {
                    "Name": "Produce"
                },
                {
                    "Name": "Vegetable"
                }
            ],
            "Aliases": [],
            "Categories": [
                {
                    "Name": "Food and Beverage"
                }
            ]
        },
        {
            "Name": "Vegetable",
            "Confidence": 99.82061767578125,
            "Instances": [],
            "Parents": [
                {
                    "Name": "Food"
                },
                {
                    "Name": "Plant"
                },
                {
                    "Name": "Produce"
                }
            ],
            "Aliases": [],
            "Categories": [
                {
                    "Name": "Food and Beverage"
                }
            ]
        },
        {
            "Name": "Box",
            "Confidence": 98.05333709716797,
            "Instances": [
                {
                    "BoundingBox": {
                        "Width": 0.9999070167541504,
                        "Height": 0.9953859448432922,
                        "Left": 3.555297735147178e-05,
                        "Top": 0.004614075645804405
                    },
                    "Confidence": 98.05333709716797
                }
            ],
            "Parents": [],
            "Aliases": [],
            "Categories": [
                {
                    "Name": "Apparel and Accessories"
                }
            ]
        },
        {
            "Name": "Fruit",
            "Confidence": 72.15345764160156,
            "Instances": [],
            "Parents": [
                {
                    "Name": "Food"
                },
                {
                    "Name": "Plant"
                },
                {
                    "Name": "Produce"
                }
            ],
            "Aliases": [],
            "Categories": [
                {
                    "Name": "Food and Beverage"
                }
            ]
        }
    ],
    "LabelModelVersion": "3.0"
}
"""