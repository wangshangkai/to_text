import argparse
from pathlib import Path


def process_file(path: Path, out):
    out.write(f"// file: {path.name}\n\n")
    out.write(path.read_text(encoding="utf-8", errors="ignore"))
    out.write("\n")


def main():
    parser = argparse.ArgumentParser(description="将文件或目录中的文件内容汇总写入一个 txt 文件。")
    parser.add_argument("input", help="待处理的路径或文件名")
    parser.add_argument("output", help="输出的 txt 文件名")
    args = parser.parse_args()

    target = Path(args.input)
    if not target.exists():
        print(f"错误: 找不到路径或文件: {target}")
        return 1

    output = Path(args.output)
    if output.parent and not output.parent.exists():
        output.parent.mkdir(parents=True, exist_ok=True)

    files = []
    if target.is_dir():
        files = sorted(p for p in target.rglob("*") if p.is_file())
    else:
        files = [target]

    with output.open("w", encoding="utf-8") as out:
        for f in files:
            process_file(f, out)

    print(f"已写入 {len(files)} 个文件到 {output}")
    return 0


if __name__ == "__main__":
    main()
