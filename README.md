# AI Fullstack

## 项目目标

待补充：未来 12 周的项目目标。

## 当前目录结构

```text
ai_fullstack/
├── app/
│   └── main.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── eval/
├── notebooks/
├── scripts/
├── tests/
├── docs/
├── requirements.txt
├── README.md
└── .gitignore
```

## 环境安装

创建并使用虚拟环境：

```bash
python -m venv .venv
source .venv/Scripts/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

如果不激活虚拟环境，也可以直接使用：

```bash
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

## 启动方式

在项目根目录运行：

```bash
.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

启动后访问：

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
```

## 导入原始文档

把 `.md` 或 `.txt` 文件放入 `data/raw/`，然后在项目根目录运行：

```bash
python scripts/import_markdown.py
```

脚本会读取非空文件，并输出到：

```text
data/processed/documents.jsonl
```

每一行是一条 JSON 记录，包含 `id`、`source_path`、`title`、`text` 和 `metadata.file_type`。

## 从零开始运行

在一台新机器上，可以按下面步骤运行项目：

```bash
git clone <repo-url>
cd ai_fullstack
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

其中 `<repo-url>` 需要替换为实际的远程仓库地址。

## 今日完成内容

- 创建项目目录结构。
- 初始化 Git 仓库。
- 创建 Python 虚拟环境 `.venv`。
- 安装第一批依赖：FastAPI、Uvicorn、Pydantic。
- 生成 `requirements.txt`。
- 创建 `app/main.py`。
- 实现 `/` 和 `/health` 两个接口。
- 配置 `.gitignore`，忽略 `.venv/` 和 Python 缓存文件。

## 参考资料

- [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Python venv 官方文档](https://docs.python.org/3/library/venv.html)

