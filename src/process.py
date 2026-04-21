import argparse
import json
from itertools import islice
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_PATH = ROOT_DIR / "docs" / "cleaned_decompile_ghidra_100k.jsonl"
DEFAULT_OUTPUT_PATH = ROOT_DIR / "docs" / "cleaned_decompile_ghidra_100k_top500.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render the first N JSONL records into a readable Markdown file."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help=f"Path to the JSONL file. Default: {DEFAULT_INPUT_PATH}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Path to the generated Markdown file. Default: {DEFAULT_OUTPUT_PATH}",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="How many JSONL records to render. Default: 500",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the generated Markdown to stdout in addition to writing the file.",
    )
    return parser.parse_args()


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip("\n")
    return str(value).strip("\n")


def read_jsonl_records(path: Path, limit: int) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as file:
        for line in islice(file, limit):
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def render_record(index: int, record: dict) -> str:
    category = normalize_text(record.get("category")) or "unknown"
    source = normalize_text(record.get("source"))
    target = normalize_text(record.get("target"))

    return "\n".join(
        [
            f"## {index}. {category}",
            "",
            f"- Category: `{category}`",
            "",
            "### Source",
            "```c",
            source,
            "```",
            "",
            "### Target",
            "```c",
            target,
            "```",
            "",
            "---",
            "",
        ]
    )


def render_markdown(input_path: Path, records: list[dict], limit: int) -> str:
    lines = [
        "# JSONL 前 500 条 Markdown 预览" if limit == 500 else f"# JSONL 前 {limit} 条 Markdown 预览",
        "",
        f"- Source file: `{input_path}`",
        f"- Rendered records: `{len(records)}`",
        "",
    ]

    for index, record in enumerate(records, start=1):
        lines.append(render_record(index, record))

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    records = read_jsonl_records(args.input, args.limit)
    markdown = render_markdown(args.input, records, args.limit)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")

    if args.stdout:
        print(markdown, end="")

    print(f"Generated Markdown: {args.output}")
    print(f"Rendered records: {len(records)}")


if __name__ == "__main__":
    main()
