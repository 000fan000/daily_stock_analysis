# 技术指标增强功能测试指南

## 📋 概述

本指南帮助您测试新增的技术指标功能，包括 MA60/MA250、KDJ、布林带、动量指标和量均线。

## 🚀 快速开始

### 1. 环境准备

确保您在项目根目录下，并已安装必要的依赖：

```bash
# 检查 Python 版本 (需要 3.7+)
python3 --version

# 安装依赖 (如果需要)
pip3 install pandas numpy

# 验证项目结构
ls -la
```

### 2. 快速验证

运行快速验证脚本检查基础功能：

```bash
python3 quick_test.py
```

预期输出：
- ✅ 所有技术指标检查通过
- 📈 显示具体的指标数值
- 🎯 显示交易信号分析
- 🎉 显示"所有技术指标测试通过！"

## 🧪 详细测试

### 3. 模拟数据测试

测试不同市场场景下的技术指标：

```bash
# 测试所有场景
python3 test_technical_indicators.py --scenarios

# 测试模拟数据
python3 test_technical_indicators.py --mock

# 运行完整测试套件
python3 test_technical_indicators.py --all
```

### 4. 真实股票数据测试

使用真实股票数据进行测试：

```bash
# 测试平安银行 (000001)
python3 test_technical_indicators.py --real 000001

# 测试贵州茅台 (600519)
python3 test_technical_indicators.py --real 600519

# 测试比亚迪 (002594)
python3 test_technical_indicators.py --real 002594
```

## 📊 测试内容详解

### 4.1 技术指标验证

脚本会验证以下新增指标：

| 指标类型 | 具体指标 | 验证内容 |
|---------|---------|---------|
| **长期均线** | MA250 | 数值合理性，趋势判断 |
| **乖离率** | MA60/MA250 Bias | 计算准确性 |
| **KDJ指标** | K, D, J 值 | 超买超卖信号 |
| **布林带** | 上中下轨 | 价格位置判断 |
| **动量指标** | 5日/10日动量 | 涨跌动能 |
| **量均线** | 5/10/20日量均 | 量价配合 |

### 4.2 提示词集成测试

验证 AI 分析提示词包含：
- ✅ MA60/MA250 显示
- ✅ KDJ 指标分析表
- ✅ 布林带分析表
- ✅ 动量指标分析表
- ✅ 量均线分析表
- ✅ 增强的决策检查清单

## 🔍 故障排除

### 常见问题

#### 问题 1: 导入错误
```bash
ImportError: cannot import name 'StockTrendAnalyzer'
```

**解决方案：**
```bash
# 确保在正确目录
cd /path/to/daily_stock_analysis

# 检查文件结构
ls -la src/stock_analyzer.py
```

#### 问题 2: 数据不足
```
⚠️ 可能数据缺失: ['MA250', 'BB_Width']
```

**解决方案：**
- 需要至少 300 天数据计算 MA250
- 需要至少 20 天数据计算布林带

#### 问题 3: 真实数据获取失败
```
❌ 无法获取 000001 的数据
```

**解决方案：**
```bash
# 检查网络连接
ping finance.sina.com.cn

# 验证数据源配置
python3 -c "
from data_provider import DataFetcherManager
manager = DataFetcherManager()
print('Available fetchers:', [f.name for f in manager.fetchers])
"
```

### 手动验证步骤

如果自动测试失败，可以手动验证：

```python
import sys
sys.path.append('src')
from stock_analyzer import StockTrendAnalyzer
import pandas as pd
import numpy as np

# 创建测试数据
analyzer = StockTrendAnalyzer()

# 手动生成数据
dates = pd.date_range(start='2024-01-01', periods=300, freq='D')
prices = np.random.randn(300).cumsum() + 100

df = pd.DataFrame({
    'date': dates,
    'close': prices,
    'volume': np.random.randint(1000000, 5000000, 300)
})

# 测试分析
result = analyzer.analyze(df, 'TEST')

# 检查指标
print(f"MA250: {result.ma250}")
print(f"KDJ_K: {result.kdj_k}")
print(f"BB_Upper: {result.bb_upper}")
```

## 📈 预期结果示例

### 成功测试输出：

```
🎉 所有技术指标测试通过！

📈 关键指标数值:
  当前价格: 12.45
  MA250: 10.89
  MA60乖离率: +2.34%
  KDJ: K=65.2, D=60.1, J=75.4
  布林带: 上=13.20, 中=12.10, 下=11.00
  动量: 5日=+2.5%, 10日=+8.3%
  量均线: 5日=4,500,000, 10日=4,200,000

🎯 交易信号:
  趋势状态: 多头排列
  买入信号: 买入
  系统评分: 75/100
  KDJ信号: KDJ强势区域
  布林带位置: 中轨之上（多头区域）
  动量信号: 强势上涨
  量趋势: 量均线多头排列，资金活跃
```

## 🔄 持续测试

### 定期验证

建议定期运行测试确保功能正常：

```bash
# 每日快速检查
python3 quick_test.py

# 每周完整测试
python3 test_technical_indicators.py --all

# 更新代码后
git pull
python3 test_technical_indicators.py --scenarios
```

### 性能监控

```bash
# 测试计算性能
time python3 test_technical_indicators.py --mock

# 内存使用监控
python3 -c "
import psutil
import sys
sys.path.append('src')
from test_technical_indicators import TechnicalIndicatorsTester
tester = TechnicalIndicatorsTester()
tester.run_comprehensive_test()
print(f'Memory used: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB')
"
```

## 🤝 贡献反馈

如果测试中遇到问题：

1. **记录错误信息**：保存完整的错误日志
2. **环境信息**：Python版本、操作系统、依赖版本
3. **测试数据**：复现问题的具体步骤

```bash
# 收集环境信息
python3 --version
pip3 list | grep -E "(pandas|numpy)"
uname -a

# 运行诊断
python3 test_technical_indicators.py --all > test_output.log 2>&1
```

## 📚 相关文档

- [技术指标实现说明](docs/technical_indicators.md)
- [AI分析配置指南](docs/ai_analysis.md)
- [数据源配置](docs/data_sources.md)

---

🎯 **目标**：确保所有技术指标计算准确，AI分析提示词完整，为用户提供可靠的股票分析服务。