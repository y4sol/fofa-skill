#!/bin/bash
# FOFA Skill 环境初始化脚本
# 用法: ./setup_venv.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "[FOFA] 初始化虚拟环境..."

# 创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "[FOFA] 虚拟环境已创建: $VENV_DIR"
else
    echo "[FOFA] 虚拟环境已存在"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 安装依赖
echo "[FOFA] 安装依赖..."
pip install --upgrade pip -q
pip install -r "$SCRIPT_DIR/requirements.txt" -q

echo "[FOFA] 环境就绪!"
echo ""
echo "用法:"
echo "  source $VENV_DIR/bin/activate"
echo "  python $SCRIPT_DIR/fofa_query.py search 'domain=example.com'"
echo ""
echo "或者直接运行:"
echo "  $VENV_DIR/bin/python $SCRIPT_DIR/fofa_query.py search 'domain=example.com'"
