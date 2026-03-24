---
name: data-processing
description: Process and transform data files with various formats
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["python3", "jq"] }
      }
  }
---

# Data Processing Skill

Process and transform data files between various formats (JSON, CSV, XML, YAML).

## Capabilities

- Format conversion (JSON ↔ CSV ↔ XML ↔ YAML)
- Data filtering and extraction
- Statistical analysis
- Data validation

## Usage

### JSON to CSV

```bash
# Using jq for simple cases
cat data.json | jq -r '.[] | [.field1, .field2] | @csv' > output.csv

# Using Python for complex transformations
python3 {baseDir}/scripts/json_to_csv.py input.json output.csv
```

### CSV to JSON

```bash
python3 -c "
import csv, json
with open('input.csv') as f:
    data = list(csv.DictReader(f))
print(json.dumps(data, indent=2))
"
```

### Filter Data

```bash
# Filter JSON by condition
cat data.json | jq '.[] | select(.status == \"active\")'

# Filter CSV
python3 {baseDir}/scripts/filter_csv.py input.csv "column=value" output.csv
```

### Statistics

```bash
# Basic statistics on numeric column
cat data.csv | python3 -c "
import csv, statistics
with open('/dev/stdin') as f:
    values = [float(row['column']) for row in csv.DictReader(f)]
print(f'Mean: {statistics.mean(values):.2f}')
print(f'Median: {statistics.median(values):.2f}')
print(f'Std Dev: {statistics.stdev(values):.2f}')
"
```

## Workflow Example

User: "Convert this JSON file to CSV and calculate the average price"

1. Read the JSON file
2. Extract the relevant fields
3. Convert to CSV format
4. Calculate statistics
5. Present results with the output file path

## Error Handling

- **Invalid format**: Detect format and suggest conversion
- **Missing fields**: Report which fields are missing
- **Large files**: Use streaming for files > 100MB
- **Encoding issues**: Try UTF-8, then common encodings

## Output

- Always show a preview (first 5-10 rows)
- Report file size and row count
- Include any statistics calculated