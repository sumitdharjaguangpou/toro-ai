# backtest_page.py - Full Backtest Studio

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from backtest_engine import BacktestEngine, BacktestVisualizer

def render_backtest_page(brain, stock):
    """Full backtest studio page"""
    
    st.markdown("# 📊 Backtest Studio")
    st.markdown("---")
    
    # Header with stock info
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"### 🔍 Backtesting: **{stock}**")
        st.caption("Simulate TORO AI performance on historical data")
    with col_h2:
        if st.button("← BACK TO DASHBOARD", use_container_width=True):
            st.session_state['show_backtest_page'] = False
            st.rerun()
    
    st.markdown("---")
    
    # ==========================================
    # BACKTEST CONTROLS
    # ==========================================
    st.markdown("### ⚙️ Backtest Configuration")
    
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    
    with col_c1:
        backtest_period = st.selectbox(
            "📅 Time Period",
            ["1 Year", "2 Years", "3 Years", "5 Years", "10 Years", "MAX"],
            index=2,
            help="Select historical period for backtest"
        )
    
    with col_c2:
        backtest_capital = st.number_input(
            "💰 Initial Capital (₹)", 
            value=100000, 
            step=50000,
            min_value=10000,
            help="Starting capital for simulation"
        )
    
    with col_c3:
        backtest_commission = st.number_input(
            "💸 Brokerage (%)",
            value=0.05,
            step=0.01,
            min_value=0.0,
            max_value=1.0,
            help="Brokerage per trade"
        ) / 100
    
    with col_c4:
        backtest_slippage = st.number_input(
            "📉 Slippage (%)",
            value=0.1,
            step=0.05,
            min_value=0.0,
            max_value=1.0,
            help="Price slippage per trade"
        ) / 100
    
    # Advanced options expander
    with st.expander("🔧 Advanced Options"):
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            max_position_pct = st.slider("Max Position Size (%)", 10, 50, 30, 5)
        with col_a2:
            trailing_activation = st.slider("Trailing Stop Activation (%)", 2, 15, 8, 1)
        with col_a3:
            min_rr_ratio = st.slider("Minimum Risk:Reward", 1.0, 3.0, 1.5, 0.1)
    
    # Run backtest button
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        run_backtest = st.button("🚀 RUN BACKTEST", use_container_width=True, type="primary")
    
    if run_backtest:
        with st.spinner("Running backtest simulation..."):
            # Map period to years
            period_map = {
                "1 Year": 1, "2 Years": 2, "3 Years": 3, 
                "5 Years": 5, "10 Years": 10, "MAX": 15
            }
            years = period_map.get(backtest_period, 5)
            
            # Calculate start date
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years * 365)
            
            # Fetch historical data
            ticker = yf.Ticker(stock)
            hist_data = ticker.history(start=start_date, end=end_date, interval="1d")
            
            if not hist_data.empty:
                hist_data = brain.calculate_all_indicators(hist_data)
                backtest = BacktestEngine(
                    initial_capital=backtest_capital,
                    commission=backtest_commission,
                    slippage=backtest_slippage
                )
                
                def get_levels(data):
                    return brain.calculate_advanced_risk_levels(data)
                
                def get_signal(data, levels):
                    return brain.get_signal_from_brain(data, levels)
                
                results = backtest.run_backtest(hist_data, get_levels, get_signal)
                st.session_state['backtest_results'] = results
                st.session_state['backtest_params'] = {
                    'years': years,
                    'capital': backtest_capital,
                    'commission': backtest_commission,
                    'slippage': backtest_slippage
                }
                st.success("✅ Backtest complete! Scroll down to view results.")
            else:
                st.error("Insufficient historical data for backtest")
    
    # ==========================================
    # DISPLAY RESULTS
    # ==========================================
    if 'backtest_results' in st.session_state:
        results = st.session_state['backtest_results']
        metrics = results['metrics']
        params = st.session_state.get('backtest_params', {})
        
        st.markdown("---")
        st.markdown("# 📈 Backtest Results")
        
        # ==========================================
        # SUMMARY CARDS
        # ==========================================
        st.markdown("### 📊 Performance Summary")
        
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        
        with col_s1:
            return_color = "#00ff88" if results['total_return'] > 0 else "#ff1744"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0a0e27, #1a1f3a); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid rgba(0,255,255,0.2);">
                <div style="font-size: 11px; color: #8892b0;">💰 TOTAL RETURN</div>
                <div style="font-size: 32px; font-weight: 800; color: {return_color};">{results['total_return']:.1f}%</div>
                <div style="font-size: 12px; color: #64748b;">₹{results['final_capital']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_s2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0a0e27, #1a1f3a); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid rgba(0,255,255,0.2);">
                <div style="font-size: 11px; color: #8892b0;">🎯 WIN RATE</div>
                <div style="font-size: 32px; font-weight: 800; color: #00ff88;">{metrics['win_rate']:.1f}%</div>
                <div style="font-size: 12px; color: #64748b;">{metrics['winning_trades']} / {metrics['total_trades']} trades</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_s3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0a0e27, #1a1f3a); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid rgba(0,255,255,0.2);">
                <div style="font-size: 11px; color: #8892b0;">📈 PROFIT FACTOR</div>
                <div style="font-size: 32px; font-weight: 800; color: #ffd700;">{metrics['profit_factor']:.2f}</div>
                <div style="font-size: 12px; color: #64748b;">Profit/Loss Ratio</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_s4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0a0e27, #1a1f3a); border-radius: 15px; padding: 15px; text-align: center; border: 1px solid rgba(0,255,255,0.2);">
                <div style="font-size: 11px; color: #8892b0;">⚡ SHARPE RATIO</div>
                <div style="font-size: 32px; font-weight: 800; color: #ffd700;">{metrics['sharpe_ratio']:.2f}</div>
                <div style="font-size: 12px; color: #64748b;">Risk-Adjusted</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ==========================================
        # DETAILED METRICS
        # ==========================================
        st.markdown("---")
        st.markdown("### 📋 Detailed Metrics")
        
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        
        with col_d1:
            st.metric("📊 Total Trades", metrics['total_trades'])
            st.metric("📈 Avg Return", f"{metrics['avg_return_pct']:.2f}%")
        
        with col_d2:
            st.metric("🏆 Avg Win", f"+{metrics['avg_win_pct']:.2f}%")
            st.metric("💀 Avg Loss", f"{metrics['avg_loss_pct']:.2f}%")
        
        with col_d3:
            st.metric("📉 Max Drawdown", f"{metrics.get('max_drawdown', 0):.1f}%")
            st.metric("📊 Expectancy", f"{metrics['expectancy_pct']:.2f}%")
        
        with col_d4:
            st.metric("⏱️ Avg Days Held", f"{metrics['avg_days_held']:.0f}")
            st.metric("🔝 Largest Win", f"+{metrics['largest_win_pct']:.1f}%")
        
        # ==========================================
        # EQUITY CURVE CHART
        # ==========================================
        st.markdown("---")
        st.markdown("### 📈 Equity Curve Analysis")
        
        fig = BacktestVisualizer.create_equity_chart(
            results['equity_curve'], 
            results['trades'], 
            backtest_capital
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # ==========================================
        # BENCHMARK COMPARISON
        # ==========================================
        st.markdown("---")
        st.markdown("### 🏆 Benchmark Comparison")
        
        try:
            nifty = yf.Ticker("^NSEI")
            nifty_data = nifty.history(start=start_date, end=end_date)
            if not nifty_data.empty:
                nifty_return = (nifty_data['Close'].iloc[-1] - nifty_data['Close'].iloc[0]) / nifty_data['Close'].iloc[0] * 100
                
                col_bench1, col_bench2 = st.columns(2)
                
                with col_bench1:
                    st.metric("TORO AI Return", f"{results['total_return']:.1f}%")
                    st.metric("TORO AI Win Rate", f"{metrics['win_rate']:.1f}%")
                    st.metric("TORO AI Sharpe", f"{metrics['sharpe_ratio']:.2f}")
                
                with col_bench2:
                    st.metric("NIFTY 50 Return", f"{nifty_return:.1f}%")
                    st.metric("NIFTY 50 Win Rate", "~50% (Buy & Hold)")
                    st.metric("NIFTY 50 Sharpe", "~0.8-1.0")
                
                if nifty_return > results['total_return']:
                    st.warning(f"⚠️ NIFTY outperformed TORO AI by {(nifty_return - results['total_return']):.1f}%")
                else:
                    st.success(f"✅ TORO AI outperformed NIFTY by {(results['total_return'] - nifty_return):.1f}%")
        except:
            st.info("NIFTY comparison not available")
        
        # ==========================================
        # TRADE LOG
        # ==========================================
        st.markdown("---")
        st.markdown("### 📋 Full Trade Log")
        
        if not results['trades'].empty:
            # Filters
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                trade_filter = st.selectbox("Filter by Result", ["All", "Winning Trades", "Losing Trades"])
            with col_f2:
                sort_by = st.selectbox("Sort by", ["Date", "Return %", "P&L", "Days Held"])
            with col_f3:
                sort_order = st.selectbox("Order", ["Descending", "Ascending"])
            
            # Apply filters
            trade_df = results['trades'].copy()
            if trade_filter == "Winning Trades":
                trade_df = trade_df[trade_df['return_pct'] > 0]
            elif trade_filter == "Losing Trades":
                trade_df = trade_df[trade_df['return_pct'] <= 0]
            
            # Apply sorting
            sort_col = {'Date': 'entry_date', 'Return %': 'return_pct', 'P&L': 'pnl', 'Days Held': 'days_held'}[sort_by]
            ascending = (sort_order == "Ascending")
            trade_df = trade_df.sort_values(sort_col, ascending=ascending)
            
            # Display dataframe
            st.dataframe(
                trade_df[['entry_date', 'exit_date', 'entry_price', 'exit_price', 
                          'return_pct', 'pnl', 'reason', 'days_held']],
                use_container_width=True,
                height=400
            )
            
            # Trade statistics
            st.markdown("---")
            col_ts1, col_ts2, col_ts3 = st.columns(3)
            
            with col_ts1:
                best_trade = results['trades'].loc[results['trades']['return_pct'].idxmax()]
                st.metric("🏆 Best Trade", f"+{best_trade['return_pct']:.1f}%", 
                         f"₹{best_trade['pnl']:,.0f}")
            
            with col_ts2:
                worst_trade = results['trades'].loc[results['trades']['return_pct'].idxmin()]
                st.metric("💀 Worst Trade", f"{worst_trade['return_pct']:.1f}%",
                         f"₹{worst_trade['pnl']:,.0f}")
            
            with col_ts3:
                avg_win = trade_df[trade_df['return_pct'] > 0]['return_pct'].mean() if len(trade_df[trade_df['return_pct'] > 0]) > 0 else 0
                avg_loss = trade_df[trade_df['return_pct'] < 0]['return_pct'].mean() if len(trade_df[trade_df['return_pct'] < 0]) > 0 else 0
                st.metric("📊 Win/Loss Ratio", f"{(avg_win / abs(avg_loss)):.2f}" if avg_loss != 0 else "N/A")
    
    # Footer
    st.markdown("---")
    st.caption("⚡ TORO AI Backtest Studio | Historical performance simulation | Past performance doesn't guarantee future results")