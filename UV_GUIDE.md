# UV包管理器使用指南

## 安装uv

如果你还没有安装uv，可以通过以下方式安装：

### Windows (推荐使用PowerShell)
```powershell
# 使用官方安装脚本
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或者使用pip安装
pip install uv
```

### 验证安装
```bash
uv --version
```

## 项目依赖管理

### 安装项目依赖
```bash
# 创建虚拟环境并安装依赖
uv sync

# 或者仅安装依赖（如果已有虚拟环境）
uv pip install -e .
```

### 添加新依赖
```bash
# 添加运行时依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 添加具体版本
uv add "package-name>=1.0,<2.0"
```

### 移除依赖
```bash
uv remove package-name
```

### 更新依赖
```bash
# 更新所有依赖
uv sync --upgrade

# 更新特定依赖
uv add --upgrade package-name
```

## 运行项目

### 方式1：直接运行脚本
```bash
# 运行PID调参工具
uv run python pid_tuner.py

# 运行测试接收器
uv run python test_receiver.py
```

### 方式2：使用项目脚本（推荐）
```bash
# 运行PID调参工具
uv run pid-tuner

# 运行测试接收器  
uv run pid-receiver
```

## 开发环境

### 安装开发依赖
```bash
# 安装所有依赖（包括开发依赖）
uv sync --all-extras

# 或者明确安装开发依赖
uv sync --extra dev
```

### 代码格式化和检查
```bash
# 格式化代码
uv run black .

# 检查代码风格
uv run flake8 .

# 类型检查
uv run mypy .

# 运行测试
uv run pytest
```

## UV的优势

### 🚀 速度极快
- 比pip快10-100倍的安装速度
- 并行下载和安装依赖
- 智能缓存机制

### 🔒 可靠的依赖解析
- 先进的依赖解析算法
- 生成lockfile确保环境一致性
- 避免依赖冲突

### 🛠️ 现代化工具
- 统一的项目管理体验
- 内置虚拟环境管理
- 支持Python版本管理

## 项目结构更新

现在项目支持以下文件：
- `pyproject.toml` - 项目配置和依赖定义
- `uv.lock` - 锁定文件（自动生成）
- `requirements.txt` - 保留用于向后兼容

## 迁移步骤

如果你之前使用pip和requirements.txt，现在可以这样迁移：

1. 安装uv
2. 在项目目录运行：`uv sync`
3. 以后使用uv命令管理依赖

## 常用命令对比

| 功能 | pip | uv |
|------|-----|-----|
| 安装依赖 | `pip install -r requirements.txt` | `uv sync` |
| 添加依赖 | 手动编辑requirements.txt + pip install | `uv add package-name` |
| 运行脚本 | `python script.py` | `uv run python script.py` |
| 创建虚拟环境 | `python -m venv venv` | 自动处理 |
| 激活环境 | `source venv/bin/activate` | 不需要 |