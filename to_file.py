import argparse
import re
from pathlib import Path


def parse(text: str):
    pattern = re.compile(r"^// file: (.*)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    files = []
    for i, m in enumerate(matches):
        name = m.group(1).strip()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[m.end():end]
        if content.startswith("\n\n"):
            content = content[2:]
        elif content.startswith("\n"):
            content = content[1:]
        if content.endswith("\n"):
            content = content[:-1]
        files.append((name, content))
    return files


def main(input_path: str, output_dir: str):
    source = Path(input_path)
    if not source.is_file():
        print(f"错误: 找不到文件: {source}")
        return 1

    files = parse(source.read_text(encoding="utf-8"))
    if not files:
        print("警告: 未找到任何 // file: 标记")
        return 1

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)

    for name, content in files:
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")

    print(f"已还原 {len(files)} 个文件到 {root}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从汇总 txt 中还原各文件到新文件夹。")
    parser.add_argument("input", help="待读取的 txt 文件")
    parser.add_argument("output", help="输出文件夹")
    args = parser.parse_args()
    main(args.input, args.output)
