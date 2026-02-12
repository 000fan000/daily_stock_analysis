#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试脚本 - 检查技术指标数据流
==============================

调试为什么新的技术指标没有传递到LLM分析
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from stock_analyzer import StockTrendAnalyzer
from analyzer import GeminiAnalyzer

def debug_data_flow():
    """调试数据流"""
    print("🔍 调试技术指标数据流...")
    
    # 1. 生成测试数据
    analyzer = StockTrendAnalyzer()
    
    dates = pd.date_range(start='2024-01-01', periods=300, freq='D')
    np.random.seed(42)
    
    base_price = 10.0
    prices = [base_price]
    for i in range(299):
        change = np.random.randn() * 0.02 + 0.005
        prices.append(prices[-1] * (1 + change))
    
    df = pd.DataFrame({
        'date': dates,
        'open': prices,
        'high': [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
        'low': [p * (1 - np.random.uniform(0, 0.02)) for p in prices],
        'close': prices,
        'volume': [np.random.randint(2000000, 8000000) for _ in prices],
    })
    
    print(f"📊 生成了 {len(df)} 天的测试数据")
    
    # 2. 分析数据
    result = analyzer.analyze(df, 'DEBUG001')
    
    print(f"\n🔬 技术指标分析结果:")
    print(f"  MA60: {result.ma60}")
    print(f"  MA250: {result.ma250}")
    print(f"  KDJ: K={result.kdj_k}, D={result.kdj_d}, J={result.kdj_j}")
    print(f"  布林带: 上={result.bb_upper}, 下={result.bb_lower}")
    print(f"  动量: 5日={result.momentum_5d}%, 10日={result.momentum_10d}%")
    
    # 3. 检查 to_dict() 是否包含新指标
    result_dict = result.to_dict()
    
    print(f"\n📋 to_dict() 包含的新指标:")
    new_indicators = [
        'ma60', 'ma250', 'bias_ma60', 'bias_ma250',
        'kdj_k', 'kdj_d', 'kdj_j', 'kdj_signal',
        'bb_upper', 'bb_middle', 'bb_lower', 'bb_width', 'bb_position',
        'momentum_5d', 'momentum_10d', 'momentum_signal',
        'vol_ma5', 'vol_ma10', 'vol_ma20', 'vol_ratio_ma5', 'vol_trend'
    ]
    
    missing_in_dict = []
    for indicator in new_indicators:
        if indicator in result_dict:
            print(f"  ✅ {indicator}: {result_dict[indicator]}")
        else:
            print(f"  ❌ {indicator}: 缺失")
            missing_in_dict.append(indicator)
    
    # 4. 测试提示词生成
    print(f"\n📝 测试提示词生成...")
    
    gemini_analyzer = GeminiAnalyzer()
    
    # 模拟pipeline的上下文构建（完全按照pipeline的逻辑）
    base_context = {
        'code': 'DEBUG001',
        'stock_name': '调试股票',
        'date': '2025-02-12',
        'today': {
            'close': result.current_price,
            'open': result.current_price * 0.98,
            'high': result.current_price * 1.02,
            'low': result.current_price * 0.99,
            'pct_chg': 2.5,
            'volume': 5000000,
            'amount': 50000000,
            'ma5': result.ma5,
            'ma10': result.ma10,
            'ma20': result.ma20,
            # 注意：pipeline会从trend_result添加ma60和ma250
        }
    }
    
    # 模拟pipeline的enhance_context逻辑
    enhanced_context = base_context.copy()
    enhanced_context['today'].update({
        'ma60': result.ma60,
        'ma250': result.ma250,
    })
    enhanced_context['trend_analysis'] = result_dict
    
    context = enhanced_context
    
    try:
        prompt = gemini_analyzer._format_prompt(context, '调试股票')
        
        print(f"✅ 提示词生成成功 (长度: {len(prompt)} 字符)")
        
        # 检查提示词是否包含新指标
        print(f"\n🔍 检查提示词中的新指标...")
        
        # 检查主要部分
        main_sections = ['MA60', 'MA250', 'KDJ', '布林带', '动量指标', '量均线']
        missing_in_prompt = []
        
        for check in main_sections:
            if check in prompt:
                print(f"  ✅ {check}: 存在")
            else:
                print(f"  ❌ {check}: 缺失")
                missing_in_prompt.append(check)
        
        # 检查具体的数值（格式化后的值）
        value_checks = [
            ('bias_ma60', f"{result.bias_ma60:+.2f}%"),
            ('bias_ma250', f"{result.bias_ma250:+.2f}%"),
            ('kdj_k', f"{result.kdj_k:.1f}"),
            ('kdj_d', f"{result.kdj_d:.1f}"),
            ('kdj_j', f"{result.kdj_j:.1f}"),
            ('bb_upper', f"{result.bb_upper:.2f}"),
            ('momentum_5d', f"{result.momentum_5d:+.2f}%"),
            ('vol_ma5', f"{result.vol_ma5:,.0f}"),
        ]
        
        for field_name, expected_value in value_checks:
            if expected_value in prompt:
                print(f"  ✅ {field_name} (值: {expected_value}): 存在")
            else:
                print(f"  ❌ {field_name} (值: {expected_value}): 缺失")
                missing_in_prompt.append(field_name)
        
        # 详细调试：显示KDJ部分的提示词内容
        print(f"\n🔍 调试：检查KDJ部分的实际内容...")
        kdj_start = prompt.find('#### KDJ 指标分析')
        if kdj_start != -1:
            kdj_end = prompt.find('####', kdj_start + 1)
            if kdj_end == -1:
                kdj_end = len(prompt)
            kdj_section = prompt[kdj_start:kdj_end]
            print("KDJ部分内容:")
            print(kdj_section[:500])  # 显示前500字符
            
            # 检查具体值
            if '83.4' in kdj_section:
                print("✅ 找到K值数值")
            else:
                print("❌ 未找到K值数值")
        
        if missing_in_prompt:
            print(f"\n❌ 提示词缺失的指标: {missing_in_prompt}")
        else:
            print(f"\n✅ 所有新指标都包含在提示词中")
            
        return len(missing_in_dict) == 0 and len(missing_in_prompt) == 0
        
    except Exception as e:
        print(f"❌ 提示词生成失败: {e}")
        return False

def simulate_pipeline_context():
    """模拟pipeline上下文构建过程"""
    print(f"\n🔄 模拟pipeline上下文构建...")
    
    # 模拟trend_analysis数据结构（来自pipeline）
    mock_trend_analysis = {
        'trend_status': '多头排列',
        'ma_alignment': 'MA5>MA10>MA20>MA60',
        'trend_strength': 75,
        'bias_ma5': 2.5,
        'bias_ma10': 3.2,
        'bias_ma20': 4.1,
        'bias_ma60': 5.8,  # 新增
        'bias_ma250': 12.3,  # 新增
        'volume_status': '放量上涨',
        'volume_trend': '量均线多头排列，资金活跃',
        'buy_signal': '买入',
        'signal_score': 78,
        'signal_reasons': ['多头排列', '量价齐升'],
        'risk_factors': ['乖离率偏高'],
        
        # 新增的技术指标（如果在pipeline中正确传递）
        'kdj_k': 65.2,
        'kdj_d': 60.1,
        'kdj_j': 75.4,
        'kdj_signal': 'KDJ强势区域',
        'bb_upper': 11.20,
        'bb_middle': 10.00,
        'bb_lower': 8.80,
        'bb_width': 24.0,
        'bb_position': '中轨之上（多头区域）',
        'momentum_5d': 2.5,
        'momentum_10d': 8.3,
        'momentum_signal': '强势上涨',
        'vol_ma5': 4500000,
        'vol_ma10': 4000000,
        'vol_ma20': 3800000,
        'vol_ratio_ma5': 1.11,
        'vol_trend': '量均线多头排列，资金活跃',
    }
    
    context = {
        'code': 'PIPELINE_TEST',
        'stock_name': 'Pipeline测试',
        'date': '2025-02-12',
        'today': {
            'close': 10.50,
            'ma5': 10.20,
            'ma10': 10.10,
            'ma20': 10.00,
            'ma60': 9.80,  # 关键：pipeline需要传递这个
            'ma250': 9.50,  # 关键：pipeline需要传递这个
        },
        'trend_analysis': mock_trend_analysis
    }
    
    gemini_analyzer = GeminiAnalyzer()
    prompt = gemini_analyzer._format_prompt(context, 'Pipeline测试')
    
    # 检查关键指标
    key_indicators = ['MA60', 'MA250', 'KDJ', '布林带', '动量指标', '量均线']
    
    print(f"📝 Pipeline模拟测试结果:")
    for indicator in key_indicators:
        if indicator in prompt:
            print(f"  ✅ {indicator}: 存在")
        else:
            print(f"  ❌ {indicator}: 缺失")
    
    return all(indicator in prompt for indicator in key_indicators)

if __name__ == "__main__":
    print("🚀 开始数据流调试...")
    
    success1 = debug_data_flow()
    success2 = simulate_pipeline_context()
    
    print(f"\n📊 调试结果:")
    print(f"  直接数据流: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"  Pipeline模拟: {'✅ 通过' if success2 else '❌ 失败'}")
    
    if success1 and success2:
        print(f"\n🎉 数据流调试成功！新指标应该能正常传递到LLM")
    else:
        print(f"\n❌ 数据流存在问题，需要修复")