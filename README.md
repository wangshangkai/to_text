# to_text / to_file

在一份 **汇总 txt** 与 **文件夹结构** 之间互相转换的两个小工具。

- `to_text.py`：把文件 / 文件夹 / 压缩包的内容汇总进一个 txt。
- `to_file.py`：读取该 txt，按标记还原出各个文件到新文件夹。

两者输出/输入的格式一致，可互相配合使用。

## 环境要求

- Python 3.8+（使用 `pathlib`、`zipfile`、`tempfile`）
- 无第三方依赖，标准库即可

## 汇总文本格式

每个文件由一行消息头 `// file: <相对路径>` 开头，下面紧跟其内容，文件之间以空行分隔：

```
// file: a.md

abcd

// file: sub/b.md

1234
```

## to_text.py

将待处理内容汇总写入一个 txt 文件。

```
python to_text.py <输入路径> <输出.txt>
```

**支持的输入：**

| 输入类型 | 行为 |
| --- | --- |
| 目录 | 递归遍历所有文件（按路径排序） |
| `.zip` / `.docx` / `.xlsx` | 解压到临时目录后，当作文件夹递归遍历 |
| 单个文件 | 只处理该文件 |

**说明：**

- 每条记录的路径是相对于遍历根目录的相对路径，如 `sub/b.md`。
- 目录/压缩包内的文件按路径排序后写入，保证输出稳定。
- 使用 UTF-8 读写，并通过 `surrogateescape` 保留无法解码的字节，二进制文件也可往返。
- 读写时不转换换行符（`newline=""`），原始 CRLF/LF 原样保留。
- 处理压缩包时使用系统临时目录，结束后自动清理。
- 示例：

```
python to_text.py ./myproject project.txt
python to_text.py ./docs.zip docs.txt
```

## to_file.py

根据汇总 txt 中的 `// file:` 标记还原各文件到新文件夹。

```
python to_file.py <输入.txt> <输出文件夹>
```

**说明：**

- 用正则 `^// file: (.*)$`（`re.MULTILINE`）定位每条消息头。
- 每个文件的内容取自「当前消息头结尾」到「下一个消息头开头」之间。
- 自动剥离消息头后的空行和末尾的分隔换行。
- 路径含子目录时（如 `sub/b.md`）会自动创建对应目录。
- 输出文件夹不存在时自动创建。

## 往返示例

```
# 汇总
python to_text.py ./myproject project.txt

# 还原到新文件夹
python to_file.py project.txt ./restored
```

`./restored` 中会重新出现 `a.md`、`sub/b.md` 等文件。

## 注意

- 汇总文本以 UTF-8 读写，字节级保留原始文件内容，`to_text` → `to_file` 往返一致。
- 内容中若出现形如 `// file: xxx` 的**独立行**，会被误判为新的文件头。如需存储这类文本，请自行调整标记规则。
