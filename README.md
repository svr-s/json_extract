# JSON Extract (`json_extract`)

A high-performance, reusable Python utility designed to natively flatten, parse, and filter deeply nested JSON data into clean, normalized Pandas DataFrames. It acts as a powerful JSON-to-CSV extraction engine for robust data pipelines.

## Features
- **Deep Hierarchical Flattening**: Uses recursive logic to safely flatten any nested JSON object, preserving exact path context via dot-notation (e.g. `parent.child.property`).
- **Cartesian List Explosion**: Intelligently handles embedded lists/arrays, exploding them into new rows to prevent data loss or complex column bloat.
- **Dynamic Filtering**: Robust API to slice your exact dataset out of massive payloads.
  - *Column Filtering*: Strict matching, 1-based numeric indexing (e.g., `["1-7", 10]`), Prefix wildcards (`parent.*`), and Suffix wildcards (`*.statusCode`).
  - *Row Filtering*: Filter rows by exact values or lists of acceptable values.
- **Smart Data Cleaning**: Natively deduplicate rows, drop `NaN`/blanks, and cleanly simplify column headers without causing naming collisions.
- **Self-Documenting Metadata**: Instantly returns schema and dimension metadata (`table_size`, `column_names` mapped by 1-based index) alongside the DataFrame.

## Requirements
- Python 3.9+
- `pandas`

---

## Installation & Usage

Import `extract_json` directly into your data pipeline script:

```python
import json
from json_extract import extract_json

# 1. Load your raw payload
with open('data.json', 'r') as f:
    payload = json.load(f)

# 2. Extract!
meta, df = extract_json(payload)
print(df.head())
```

---

## Function Reference

### `extract_json(json_data, **kwargs)`

The primary extraction engine.

#### Parameters

* **`json_data`** `(dict | list)`: **(Required)**
  The parsed JSON payload to process. It handles normal dictionaries, lists of dictionaries, or even raw primitive 2D arrays (`[[0, 1], [2, 3]]`) mapping them securely to `col1`, `col2`.

* **`desired_columns`** `(list)`: *(Optional)*
  A list of specific column names or numeric indices to retain. It natively supports numeric ranges and Unix-style wildcards (`*`, `?`).
  * **Numeric Ranges/Indices (1-based)**: `["1-7", "10", 12]` (Gets columns 1 through 7, 10, and 12). Duplicate overlaps are safely ignored.
  * **Exact Match**: `["accountId"]`
  * **Prefix Wildcard**: `["shippingAddress.*"]` (Gets all properties starting with `shippingAddress.`)
  * **Suffix Wildcard**: `["*.statusCode"]` (Gets every `statusCode` across the entire document)

* **`row_filters`** `(dict)`: *(Optional)*
  A dictionary mapping a specific column to a required value. You can supply a single exact match, or a list of matches.
  * **Exact**: `{"accountId": "ACC-99823-XYZ"}`
  * **List**: `{"regionCode": ["US-EAST", "EU-WEST"]}`

* **`remove_duplicates`** `(bool)`: *(Optional, Default: False)*
  If `True`, drops any completely identical rows generated from Cartesian explosions after all filters are applied.

* **`simplify_columns`** `(bool)`: *(Optional, Default: False)*
  If `True`, it trims away verbose parent hierarchies in the column names, leaving only the final child key (e.g., `parent.child.shortName` safely becomes `shortName`). 
  *Note: If simplifying causes a name collision (e.g., `type.code` and `name.code` both mapping to `code`), it intelligently retains the full dot-notation for those specific columns to prevent data overwrite.*

* **`remove_empty`** `(bool | str)`: *(Optional, Default: False)*
  Cleans the dataset by dropping rows polluted with missing values (`NaN`, `None`) or blank strings (`""`).
  * `'any'` (or `True`): Strict. Drops the row if *any* of the filtered columns are missing.
  * `'all'`: Lenient. Drops the row only if *all* of the filtered columns are entirely missing.
  * `False`: Disabled. Retains everything.

---

## Full Example Pipeline

Here is an example demonstrating all parameters functioning in tandem to slice a massive, nested payload down to an exact, clean specification:

```python
import json
from json_extract import extract_json

with open('users_export.json', 'r') as f:
    data = json.load(f)

# Extract only the fields we care about, exactly for our target accounts
meta, df = extract_json(
    json_data=data,
    
    # 1. Grab Account ID, specific columns by index, and shipping address properties
    desired_columns=[
        "accountId", 
        "2-4",
        "shippingAddress.*",
        "*.statusCode"
    ],
    
    # 2. Filter to just these two specific regions
    row_filters={
        "regionCode": ["US-EAST", "EU-WEST"]
    },
    
    # 3. Clean up the resulting DataFrame
    remove_duplicates=True,
    simplify_columns=True,  # Turns "shippingAddress.zipCode" into "zipCode"
    remove_empty='all'      # Drop rows that are totally blank
)

print(df.to_csv(index=False))
```
