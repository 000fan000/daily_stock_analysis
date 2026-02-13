#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt调试工具 - 打印完整的Prompt内容
====================================

用于调试和分析LLM Prompt的完整内容
包含所有变量的值，便于调试和优化
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import argparse
from datetime import datetime


def print_full_prompt(
    stock_code: str = "000001",
    stock_name: str = None,
    show_context: bool = True,
    show_sections: bool = True,
    show_technical: bool = True,
    output_file: str = None
):
    """
    打印完整的Prompt内容用于调试
    
    Args:
        stock_code: 股票代码
        stock_name: 股票名称（可选，默认自动获取）
        show_context: 显示上下文数据
        show_sections: 显示Prompt结构
        show_technical: 显示技术指标数据
        output_file: 输出文件路径（可选）
    """
    from analyzer import GeminiAnalyzer
    from stock_analyzer import StockTrendAnalyzer
    from data_provider import DataFetcherManager
    from src.storage import DatabaseManager
    import pandas as pd
    
    print("=" * 80)
    print("🔍 LLM Prompt 调试工具")
    print("=" * 80)
    print(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📌 股票代码: {stock_code}")
    print()
    
    # 1. 获取股票数据
    print("📊 步骤1: 获取股票数据...")
    db = DatabaseManager.get_instance()
    fetcher_manager = DataFetcherManager()
    
    # 获取股票名称
    if not stock_name:
        stock_name = fetcher_manager.get_stock_name(stock_code)
        if not stock_name:
            stock_name = f'股票{stock_code}'
    
    print(f"  ✅ 股票名称: {stock_name}")
    
    # 获取历史数据
    from datetime import timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    try:
        df = fetcher_manager.get_daily_data(stock_code, start_date, end_date)
        
        # Handle tuple return from some data fetchers
        if isinstance(df, tuple):
            df = df[0]
        
        if df is not None and len(df) > 0:
            print(f"  ✅ 获取到 {len(df)} 条历史数据")
        else:
            print(f"  ⚠️ 未能获取历史数据")
            df = None
    except Exception as e:
        print(f"  ❌ 获取数据失败: {e}")
        df = None
    
    # 2. 执行技术分析
    print("\n📊 步骤2: 执行技术分析...")
    trend_result = None
    
    if df is not None and len(df) > 30:
        analyzer = StockTrendAnalyzer()
        trend_result = analyzer.analyze(df, stock_code)
        print(f"  ✅ 技术分析完成")
        print(f"     - 趋势状态: {trend_result.trend_status.value}")
        print(f"     - 买入信号: {trend_result.buy_signal.value}")
        print(f"     - 评分: {trend_result.signal_score}/100")
    
    # 3. 获取实时行情
    print("\n📊 步骤3: 获取实时行情...")
    realtime_quote = None
    try:
        realtime_quote = fetcher_manager.get_realtime_quote(stock_code)
        if realtime_quote:
            print(f"  ✅ 实时行情: {realtime_quote.price}元")
        else:
            print(f"  ⚠️ 未能获取实时行情")
    except Exception as e:
        print(f"  ⚠️ 获取实时行情失败: {e}")
    
    # 4. 构建上下文
    print("\n📊 步骤4: 构建分析上下文...")
    
    context = {
        'code': stock_code,
        'stock_name': stock_name,
        'date': end_date,
        'today': {},
        'data_missing': df is None,
    }
    
    # 添加今日数据
    if df is not None and len(df) > 0:
        latest = df.iloc[-1]
        context['today'] = {
            'close': latest.get('close'),
            'open': latest.get('open'),
            'high': latest.get('high'),
            'low': latest.get('low'),
            'volume': latest.get('volume'),
            'amount': latest.get('amount'),
            'pct_chg': latest.get('pct_chg'),
            'ma5': latest.get('ma5'),
            'ma10': latest.get('ma10'),
            'ma20': latest.get('ma20'),
            'ma60': latest.get('ma60'),
            'ma250': latest.get('ma250'),
        }
    
    # 添加趋势分析结果
    if trend_result:
        context['trend_analysis'] = trend_result.to_dict()
    
    # 5. 生成Prompt
    print("\n📊 步骤5: 生成LLM Prompt...")
    
    gemini_analyzer = GeminiAnalyzer()
    
    try:
        prompt = gemini_analyzer._format_prompt(context, stock_name)
        print(f"  ✅ Prompt生成完成")
        print(f"     - 长度: {len(prompt)} 字符")
        print(f"     - 行数: {len(prompt.splitlines())} 行")
        
    except Exception as e:
        print(f"  ❌ Prompt生成失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 6. 显示详细输出
    print("\n" + "=" * 80)
    print("📝 完整Prompt内容")
    print("=" * 80)
    
    # 显示上下文数据（如果需要）
    if show_context:
        print("\n📋 上下文数据:")
        print("-" * 40)
        
        # 今日数据
        if 'today' in context and context['today']:
            print("\n【今日行情】")
            for key, value in context['today'].items():
                if value is not None:
                    print(f"  {key}: {value}")
        
        # 趋势分析
        if 'trend_analysis' in context:
            print("\n【趋势分析】")
            trend = context['trend_analysis']
            print(f"  趋势状态: {trend.get('trend_status', 'N/A')}")
            print(f"  均线排列: {trend.get('ma_alignment', 'N/A')}")
            print(f"  买入信号: {trend.get('buy_signal', 'N/A')}")
            print(f"  系统评分: {trend.get('signal_score', 0)}/100")
            
            # 显示技术指标
            if show_technical:
                print("\n【技术指标详情】")
                
                # KDJ
                if 'kdj_k' in trend:
                    print(f"  KDJ: K={trend.get('kdj_k', 0):.1f}, D={trend.get('kdj_d', 0):.1f}, J={trend.get('kdj_j', 0):.1f}")
                    print(f"    信号: {trend.get('kdj_signal', 'N/A')}")
                
                # 布林带
                if 'bb_upper' in trend:
                    print(f"  布林带: 上={trend.get('bb_upper', 0):.2f}, 中={trend.get('bb_middle', 0):.2f}, 下={trend.get('bb_lower', 0):.2f}")
                    print(f"    位置: {trend.get('bb_position', 'N/A')}")
                
                # 动量
                if 'momentum_5d' in trend:
                    print(f"  动量: 5日={trend.get('momentum_5d', 0):+.2f}%, 10日={trend.get('momentum_10d', 0):+.2f}%")
                    print(f"    信号: {trend.get('momentum_signal', 'N/A')}")
                
                # 量均线
                if 'vol_ma5' in trend:
                    print(f"  量均线: 5日={trend.get('vol_ma5', 0):,.0f}, 10日={trend.get('vol_ma10', 0):,.0f}")
                    print(f"    趋势: {trend.get('vol_trend', 'N/A')}")
    
    # 显示Prompt结构（如果需要）
    if show_sections:
        print("\n\n📑 Prompt结构:")
        print("-" * 40)
        
        lines = prompt.split('\n')
        current_section = []
        
        for i, line in enumerate(lines):
            # 检测章节标题
            if line.startswith('#'):
                if current_section:
                    print(f"  ... ({len(current_section)} lines)")
                    current_section = []
                print(f"\n{line}")
            elif i < 3:  # 显示前几行
                print(line)
        
        if len(lines) > 3:
            print(f"\n... (中间省略 {len(lines)-6} 行) ...\n")
            # 显示最后几行
            for line in lines[-3:]:
                print(line)
    
    # 显示完整Prompt
    print("\n\n" + "=" * 80)
    print("📄 完整Prompt (全文)")
    print("=" * 80)
    print(prompt)
    
    # 保存到文件（如果需要）
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Prompt调试 - {stock_code} {stock_name}\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 股票代码: {stock_code}\n")
            f.write(f"# 股票名称: {stock_name}\n")
            f.write("=" * 80 + "\n\n")
            f.write(prompt)
        
        print(f"\n💾 Prompt已保存到: {output_file}")
    
    print("\n" + "=" * 80)
    print("✅ 调试完成")
    print("=" * 80)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='LLM Prompt调试工具')
    parser.add_argument('stock_code', nargs='?', default='000001', help='股票代码 (默认: 000001)')
    parser.add_argument('--name', '-n', type=str, help='股票名称')
    parser.add_argument('--output', '-o', type=str, help='输出文件路径')
    parser.add_argument('--no-context', action='store_true', help='不显示上下文数据')
    parser.add_argument('--no-sections', action='store_true', help='不显示Prompt结构')
    parser.add_argument('--no-technical', action='store_true', help='不显示技术指标详情')
    
    args = parser.parse_args()
    
    print_full_prompt(
        stock_code=args.stock_code,
        stock_name=args.name,
        show_context=not args.no_context,
        show_sections=not args.no_sections,
        show_technical=not args.no_technical,
        output_file=args.output
    )


if __name__ == "__main__":
    main()