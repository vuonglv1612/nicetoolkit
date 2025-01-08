# Nice Tool Kit

A toolkit for my personal use.

## Installation

```bash
pip install nice-tool-kit
```

## Tools

### XML Formatter (`xmlformat`)

A command-line tool to format or minimize XML files.

#### Usage

1. Pretty format an XML file:
```bash
xmlformat input.xml output.xml
```

2. Minimize XML file:
```bash
xmlformat -m input.xml output.xml
```

3. Read from stdin and write to stdout:
```bash
cat input.xml | xmlformat - -
```

### AWS CloudWatch Logs Transformer (`awslog`)

Transform AWS CloudWatch Logs from JSON format to plain text.

#### Usage

1. Transform logs to stdout:
```bash
awslog input.json
```

2. Save transformed logs to file:
```bash
awslog input.json -o output.txt
# or
awslog input.json --output output.txt
```

#### Input JSON Format
The tool expects CloudWatch logs in JSON format with the following structure:
```json
[
  {
    "@message": {
      "log": "actual log content"
    }
  }
]
```

## Versioning

This project uses automatic versioning in format `YYYY.MM.PATCH`:
- Version is automatically bumped when commits are pushed to master
- Year and month are updated based on current date
- Patch number increases for multiple commits in same month