# 1. 安装依赖
cd AQARION
pip install -e ".[dev]"

# 2. 运行验证套件
python verification/run_all.py

# 3. 预期结果：核心测试通过，XFAIL标记的反例测试确认已知限制
