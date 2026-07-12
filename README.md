# AI Fullstack

一个用于整理 AI 学习数据、执行数据质量检查并提供 FastAPI 服务的最小工程。目前支持将 Markdown/TXT 原始资料导入 JSONL、检查处理后数据与 Golden Set，以及启动基础 Web API。

## 当前目录结构

```text
ai_fullstack/
├── app/                  # FastAPI 应用
├── data/
│   ├── raw/              # 原始 Markdown/TXT 资料
│   ├── processed/        # 导入后的 JSONL 数据
│   └── eval/             # Golden Set
├── docs/                 # 项目文档
├── notebooks/            # 探索性分析
├── reports/              # 质量检查报告
├── scripts/              # 数据导入与检查脚本
├── tests/                # 自动化测试
├── requirements.txt
├── README.md
└── .gitignore
```

## 环境要求

- Python 3.12
- Git

所有命令均在项目根目录运行。

## 安装

克隆项目并创建虚拟环境：

```bash
git clone <repo-url>
cd ai_fullstack
python -m venv .venv
```

其中 `<repo-url>` 需要替换为实际的远程仓库地址。

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS / Linux：

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

`requirements.txt` 采用完整版本锁定，其中 FastAPI、Uvicorn 和 Pydantic 是运行依赖，pytest 是开发/测试依赖，其余为这些包的传递依赖。

## 导入原始数据

将 UTF-8 编码的 `.md` 或 `.txt` 文件放入 `data/raw/`，然后运行：

```bash
python scripts/import_markdown.py --input data/raw --output data/processed/documents.jsonl
```

输出文件 `data/processed/documents.jsonl` 每行是一条 JSON 记录，包含 `id`、`source_path`、`title`、`text` 和 `metadata.file_type`。输入目录不存在或输出文件无法写入时，命令会失败；非 UTF-8 文件会被跳过并提示；空目录会生成空 JSONL 文件。

## 运行质量检查

检查处理后的数据并更新 `reports/quality_report.md`：

```bash
python scripts/check_dataset.py
```

检查 Golden Set：

```bash
python scripts/check_golden.py data/eval/golden.jsonl
```

运行自动化测试：

```bash
python -m pytest tests --basetemp .pytest_tmp
```

## 启动 API

启动开发服务器：

```bash
python -m uvicorn app.main:app --reload
```

启动后访问：

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
```
