from lxml import etree
import argparse
import sys


def format_xml(input_file, output_file, minimize=False):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(input_file, parser)
        root = tree.getroot()

        if minimize:
            for elem in root.iter():
                if elem.tail is not None:
                    elem.tail = elem.tail.strip()
                if elem.text is not None:
                    elem.text = elem.text.strip()
            tree.write(
                output_file, pretty_print=False, xml_declaration=True, encoding="utf-8"
            )
        else:
            tree.write(
                output_file, pretty_print=True, xml_declaration=True, encoding="utf-8"
            )

        print(f"XML successfully processed and saved to {output_file}")
        return 0

    except Exception as e:
        print(f"Error processing XML: {str(e)}", file=sys.stderr)
        return 1


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Format XML files with options to minimize or prettify",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.xml output.xml             # Pretty format XML
  %(prog)s -m input.xml output.xml          # Minimize XML
  %(prog)s -m input.xml -                   # Output minimized XML to stdout
        """,
    )

    parser.add_argument("input", help="Input XML file (use '-' for stdin)")
    parser.add_argument("output", help="Output XML file (use '-' for stdout)")
    parser.add_argument(
        "-m",
        "--minimize",
        action="store_true",
        help="Minimize XML output (default: prettify)",
    )

    args = parser.parse_args(args)

    if args.input == "-":
        input_data = sys.stdin.buffer.read()
        tree = etree.fromstring(input_data)
        if args.output == "-":
            if args.minimize:
                sys.stdout.buffer.write(etree.tostring(tree, pretty_print=False))
            else:
                sys.stdout.buffer.write(etree.tostring(tree, pretty_print=True))
            return 0
        else:
            with open(args.output, "wb") as f:
                if args.minimize:
                    f.write(etree.tostring(tree, pretty_print=False))
                else:
                    f.write(etree.tostring(tree, pretty_print=True))
            return 0

    return format_xml(args.input, args.output, args.minimize)


if __name__ == "__main__":
    sys.exit(main())
