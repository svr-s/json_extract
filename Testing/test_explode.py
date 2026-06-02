from json_extract_pandas import extract_json
import json

data = [{
    "orderid": "ORD-123",
    "line_items": [
        {"sku": "L1"}, {"sku": "L2"}
    ],
    "tags": [
        {
            "code": {
                "category": ["A", "B"]
            },
            "value": ["v1", "v2"]
        },
        {
            "code": {
                "category": ["C", "D"]
            },
            "value": ["v3", "v4"]
        }
    ]
}]

# Scenario 3: Ancestor Explosion! We only ask for the deeply nested child.
print("=== Scenario 3: Ancestor Explosion ('tags.code.category') ===")
meta, df = extract_json(data, explode_paths=["tags.code.category"])
print(df.to_string())

