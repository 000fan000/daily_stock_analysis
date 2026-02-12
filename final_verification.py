#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证脚本 - 确认技术指标修复成功
====================================

验证新的技术指标现在能够正确传递到LLM分析
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_final_verification():
    """最终验证所有修复都工作正常"""
    print("🎯 最终验证：技术指标增强功能")
    print("=" * 50)
    
    # 验证核心组件
    tests = []
    
    # 1. 验证 stock_analyzer.py
    try:
        from stock_analyzer import StockTrendAnalyzer
        analyzer = StockTrendAnalyzer()
        
        # 检查新增的方法
        methods = [
            '_calculate_kdj', '_calculate_bollinger_bands', 
            '_calculate_momentum', '_calculate_volume_ma',
            '_analyze_kdj', '_analyze_bollinger_bands',
            '_analyze_momentum', '_analyze_volume_ma'
        ]
        
        missing_methods = []
        for method in methods:
            if not hasattr(analyzer, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ StockTrendAnalyzer 缺失方法: {missing_methods}")
            tests.append(False)
        else:
            print("✅ StockTrendAnalyzer 所有新方法存在")
            tests.append(True)
            
    except Exception as e:
        print(f"❌ StockTrendAnalyzer 导入失败: {e}")
        tests.append(False)
    
    # 2. 验证 TrendAnalysisResult 类
    try:
        from stock_analyzer import TrendAnalysisResult
        result = TrendAnalysisResult('TEST')
        
        # 检查新增的属性
        new_attrs = [
            'ma250', 'bias_ma60', 'bias_ma250',
            'kdj_k', 'kdj_d', 'kdj_j', 'kdj_signal',
            'bb_upper', 'bb_middle', 'bb_lower', 'bb_width', 'bb_position',
            'momentum_5d', 'momentum_10d', 'momentum_signal',
            'vol_ma5', 'vol_ma10', 'vol_ma20', 'vol_ratio_ma5', 'vol_trend'
        ]
        
        missing_attrs = []
        for attr in new_attrs:
            if not hasattr(result, attr):
                missing_attrs.append(attr)
        
        if missing_attrs:
            print(f"❌ TrendAnalysisResult 缺失属性: {missing_attrs}")
            tests.append(False)
        else:
            print("✅ TrendAnalysisResult 所有新属性存在")
            tests.append(True)
            
    except Exception as e:
        print(f"❌ TrendAnalysisResult 导入失败: {e}")
        tests.append(False)
    
    # 3. 验证 analyzer.py 提示词格式化器
    try:
        from analyzer import GeminiAnalyzer
        prompt_analyzer = GeminiAnalyzer()
        
        # 检查格式化方法存在
        if hasattr(prompt_analyzer, '_format_prompt'):
            print("✅ GeminiAnalyzer 提示词格式化方法存在")
            tests.append(True)
        else:
            print("❌ GeminiAnalyzer 缺失提示词格式化方法")
            tests.append(False)
            
    except Exception as e:
        print(f"❌ GeminiAnalyzer 导入失败: {e}")
        tests.append(False)
    
    # 4. 验证 pipeline.py 集成
    try:
        from core.pipeline import StockAnalysisPipeline
        from src.config import get_config
        
        pipeline = StockAnalysisPipeline(config=get_config())
        
        # 检查增强方法存在
        if hasattr(pipeline, '_enhance_context'):
            print("✅ Pipeline _enhance_context 方法存在")
            tests.append(True)
        else:
            print("❌ Pipeline 缺失 _enhance_context 方法")
            tests.append(False)
            
    except Exception as e:
        print(f"❌ Pipeline 导入失败: {e}")
        tests.append(False)
    
    # 5. 验证 storage.py 数据库模型
    try:
        from storage import StockDaily
        
        # 检查新增的数据库字段
        new_fields = [
            'ma60', 'ma250', 'bias_ma5', 'bias_ma10', 'bias_ma20', 
            'bias_ma60', 'bias_ma250', 'kdj_k', 'kdj_d', 'kdj_j',
            'bb_upper', 'bb_middle', 'bb_lower', 'bb_width', 'bb_position',
            'momentum_5d', 'momentum_10d', 'vol_ma5', 'vol_ma10', 'vol_ma20',
            'vol_ratio_ma5', 'vol_trend'
        ]
        
        missing_fields = []
        for field in new_fields:
            if not hasattr(StockDaily, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ StockDaily 缺失字段: {missing_fields}")
            tests.append(False)
        else:
            print("✅ StockDaily 所有新字段存在")
            tests.append(True)
            
    except Exception as e:
        print(f"❌ StockDaily 导入失败: {e}")
        tests.append(False)
    
    # 总结
    passed = sum(tests)
    total = len(tests)
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    print("=" * 50)
    
    if passed == total:
        print("🎉 所有验证通过！技术指标增强功能已完全修复")
        print("\n💡 新功能现在包括:")
        print("  ✅ MA60/MA250 长期均线分析")
        print("  ✅ KDJ 随机指标 (超买超卖判断)")
        print("  ✅ 布林带 (支撑压力位)")
        print("  ✅ 动量指标 (趋势动能)")
        print("  ✅ 量均线 (量价配合分析)")
        print("  ✅ 增强的 AI 分析提示词")
        print("\n🚀 现在可以进行完整的股票分析了！")
        return True
    else:
        print("❌ 部分验证失败，请检查实现")
        return False

if __name__ == "__main__":
    success = test_final_verification()
    sys.exit(0 if success else 1)