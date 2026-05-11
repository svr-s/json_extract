import json
from src.json_extract import extract_json

data = {
    "col1": "A",
    "col2": "B",
    "col3": "C",
    "col4": "D",
    "col5": "E",
    "col6": "F",
    "col7": "G"
}

meta, df = extract_json(data, desired_columns=["1-3", "5", "1"])
print(meta)
print(df)
