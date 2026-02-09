#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速验证脚本 - 验证技术指标增强功能
==================================

快速检查新增技术指标是否正常工作

使用方法：
python3 quick_test.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from stock_analyzer import StockTrendAnalyzer

def quick_test():
    """快速测试所有新功能"""
    print("🔍 快速验证技术指标增强功能...")
    
    # 创建测试数据
    analyzer = StockTrendAnalyzer()
    
    # 生成足够多的数据来测试所有指标
    dates = pd.date_range(start='2024-01-01', periods=300, freq='D')
    np.random.seed(42)
    
    # 创建趋势向上的数据
    base_price = 10.0
    prices = [base_price]
    for i in range(299):
        change = np.random.randn() * 0.02 + 0.005  # 轻微上涨趋势
        prices.append(prices[-1] * (1 + change))
    
    df = pd.DataFrame({
        'date': dates,
        'open': prices,
        'high': [p * (1 + np.random.uniform(0, 0.03)) for p in prices],
        'low': [p * (1 - np.random.uniform(0, 0.03)) for p in prices],
        'close': prices,
        'volume': [np.random.randint(2000000, 8000000) for _ in prices],
    })
    
    print(f"📊 生成 {len(df)} 天的测试数据")
    
    # 分析数据
    result = analyzer.analyze(df, 'TEST001')
    
    # 检查所有新增指标
    print("\n🔬 检查技术指标:")
    
    checks = [
        ("MA250长期均线", result.ma250 > 0),
        ("MA60乖离率", hasattr(result, 'bias_ma60')),
        ("MA250乖离率", hasattr(result, 'bias_ma250')),
        ("KDJ指标", result.kdj_k > 0 and result.kdj_d > 0),
        ("布林带上轨", result.bb_upper > result.bb_middle),
        ("布林带下轨", result.bb_lower < result.bb_middle),
        ("5日动量", hasattr(result, 'momentum_5d')),
        ("10日动量", hasattr(result, 'momentum_10d')),
        ("5日量均线", result.vol_ma5 > 0),
        ("量比", result.vol_ratio_ma5 > 0),
    ]
    
    all_passed = True
    for name, check in checks:
        status = "✅" if check else "❌"
        print(f"  {status} {name}")
        if not check:
            all_passed = False
    
    # 显示具体数值
    print(f"\n📈 关键指标数值:")
    print(f"  当前价格: {result.current_price:.2f}")
    print(f"  MA250: {result.ma250:.2f}")
    print(f"  MA60乖离率: {result.bias_ma60:+.2f}%")
    print(f"  KDJ: K={result.kdj_k:.1f}, D={result.kdj_d:.1f}, J={result.kdj_j:.1f}")
    print(f"  布林带: 上={result.bb_upper:.2f}, 中={result.bb_middle:.2f}, 下={result.bb_lower:.2f}")
    print(f"  动量: 5日={result.momentum_5d:+.2f}%, 10日={result.momentum_10d:+.2f}%")
    print(f"  量均线: 5日={result.vol_ma5:,.0f}, 10日={result.vol_ma10:,.0f}")
    
    # 测试信号生成
    print(f"\n🎯 交易信号:")
    print(f"  趋势状态: {result.trend_status.value}")
    print(f"  买入信号: {result.buy_signal.value}")
    print(f"  系统评分: {result.signal_score}/100")
    print(f"  KDJ信号: {result.kdj_signal}")
    print(f"  布林带位置: {result.bb_position}")
    print(f"  动量信号: {result.momentum_signal}")
    print(f"  量趋势: {result.vol_trend}")
    
    return all_passed

if __name__ == "__main__":
    if quick_test():
        print("\n🎉 所有技术指标测试通过！")
        print("\n💡 下一步:")
        print("  1. 运行完整测试: python3 test_technical_indicators.py --all")
        print("  2. 测试真实股票: python3 test_technical_indicators.py --real 000001")
        print("  3. 查看测试指南: cat TESTING_GUIDE.md")
    else:
        print("\n❌ 部分技术指标测试失败，请检查实现")
        sys.exit(1)