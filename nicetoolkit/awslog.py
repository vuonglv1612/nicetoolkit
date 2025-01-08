"""
Transform AWS CloudWatch Logs JSON to plain text
"""

#!/usr/bin/env python3
import argparse
import json
import sys
from typing import List, Dict, Any


class LogTransformer:
    def __init__(self, input_file: str, output_file: str = None):
        self.input_file = input_file
        self.output_file = output_file
        self.logs: List[Dict[str, Any]] = []

    def read_json_logs(self) -> None:
        """Read JSON logs from input file."""
        try:
            with open(self.input_file, "r") as f:
                self.logs = json.load(f)
        except FileNotFoundError:
            print(f"Error: Input file '{self.input_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{self.input_file}'.")
            sys.exit(1)

    def extract_log_content(self) -> List[str]:
        """Extract log content from the JSON structure."""
        log_lines = []
        for entry in self.logs:
            try:
                # Handle the specific structure where log content is nested
                if "@message" in entry and "log" in entry["@message"]:
                    log_lines.append(entry["@message"]["log"])
            except (KeyError, TypeError):
                print(f"Warning: Skipping malformed log entry: {entry}")
                continue
        return log_lines

    def write_output(self, log_lines: List[str]) -> None:
        """Write the transformed logs to the output destination."""
        output_content = "\n".join(log_lines)

        if self.output_file:
            try:
                with open(self.output_file, "w") as f:
                    f.write(output_content)
                print(f"Successfully wrote logs to {self.output_file}")
            except IOError as e:
                print(f"Error writing to output file: {e}")
                sys.exit(1)
        else:
            # If no output file specified, print to stdout
            print(output_content)


def main():
    parser = argparse.ArgumentParser(
        description="Transform JSON logs to plain text format.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  %(prog)s input.json
  %(prog)s input.json -o output.txt
  %(prog)s input.json --output output.txt
""",
    )

    parser.add_argument("input", help="Input JSON log file")
    parser.add_argument(
        "-o", "--output", help="Output text file (optional, defaults to stdout)"
    )

    args = parser.parse_args()

    # Create transformer instance
    transformer = LogTransformer(args.input, args.output)

    # Process the logs
    transformer.read_json_logs()
    log_lines = transformer.extract_log_content()
    transformer.write_output(log_lines)


if __name__ == "__main__":
    main()
