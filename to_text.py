import argparse
import tempfile
import zipfile
from pathlib import Path


def _write(output: Path, files: list, root: Path):
    with output.open("w", encoding="utf-8", errors="surrogateescape", newline="") as out:
        for f in files:
            name = f.relative_to(root).as_posix()
            out.write(f"// file: {name}\n\n")
            with f.open("r", encoding="utf-8", errors="surrogateescape", newline="") as src:
                out.write(src.read())
            out.write("\n\n")
    print(f"已写入 {len(files)} 个文件到 {output}")


def main(input_path: str, output_path: str):
    target = Path(input_path)
    if not target.exists():
        print(f"错误: 找不到路径或文件: {target}")
        return 1

    output = Path(output_path)
    if output.parent and not output.parent.exists():
        output.parent.mkdir(parents=True, exist_ok=True)

    if target.is_dir():
        files = sorted(p for p in target.rglob("*") if p.is_file())
        _write(output, files, target)
    elif target.is_file() and target.suffix.lower() in {".zip", ".docx", ".xlsx"}:
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(target) as zf:
                zf.extractall(tmp)
            root = Path(tmp)
            files = sorted(p for p in root.rglob("*") if p.is_file())
            _write(output, files, root)
    else:
        _write(output, [target], target.parent)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将文件或目录中的文件内容汇总写入一个 txt 文件。")
    parser.add_argument("input", help="待处理的路径或文件名")
    parser.add_argument("output", help="输出的 txt 文件名")
    args = parser.parse_args()
    main(args.input, args.output)
