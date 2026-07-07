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

## 今日完成内容

- 创建项目目录结构。
- 初始化 Git 仓库。
- 创建 Python 虚拟环境 `.venv`。
- 安装第一批依赖：FastAPI、Uvicorn、Pydantic。
- 生成 `requirements.txt`。
- 创建 `app/main.py`。
- 实现 `/` 和 `/health` 两个接口。
- 配置 `.gitignore`，忽略 `.venv/` 和 Python 缓存文件。
