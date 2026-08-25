① 创建目录
↓
② 创建虚拟环境

```python
python -m venv .venv
```

↓
③ 激活

```python
.venv\Scripts\Activate.ps1
```

↓
④ 安装依赖

```python
python -m pip install --upgrade pip
pip install fastapi uvicorn openai python-dotenv
```

↓
⑤ 保存依赖

```python
pip freeze > requirements.txt requirements.txt

pip install -r requirements.txt
```

↓
⑥ 创建项目目录
↓
⑦ 配置 .env
↓
⑧ VSCode 选择 .venv

```
Ctrl + Shift + P
Python: Select Interpreter
```

↓
⑨ 检查环境

```python
python --version
pip list
```

↓
⑩ 开始写代码
↓
⑪ 启动

```python
uvicorn app.main:app --reload
```

`主要理解`
↓
项目
├── 环境
├── 依赖
├── 配置
├── Router
├── Schema
├── Service
└── Application
