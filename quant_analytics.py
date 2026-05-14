# quant_analytics.py
# ==========================================
# ADVANCED QUANTITATIVE ANALYTICS DISPLAY
# Institutional-grade mathematical models
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np


def render_quant_analytics(brain, data, levels):
    """
    Render advanced quantitative analytics
    Includes: Hurst Exponent, Entropy, Z-Score, Bayesian, VaR, etc.
    """
    
    # ==========================================
    # ADVANCED MATHEMATICS (Expandable)
    # ==========================================
    with st.expander("📊 QUANT ANALYTICS", expanded=False):
        
        # ==========================================
        # TRY TO GET ADVANCED QUANT DATA
        # ==========================================
        try:
            # Get advanced quant analysis from brain
            quant_data = brain.get_quant_analysis(data)
            
            if 'error' not in quant_data:
                
                # ==========================================
                # ROW 1: HURST, ENTROPY, Z-SCORE
                # ==========================================
                st.markdown(
                    "<div style='font-size: 11px; color: #8892b0; margin-bottom: 10px;'>🔬 ADVANCED QUANT MODELS</div>",
                    unsafe_allow_html=True
                )
                
                col1, col2, col3 = st.columns(3)
                
                # Hurst Exponent
                with col1:
                    h = quant_data['hurst']
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">{h['icon']} HURST EXPONENT</div>
                        <div class="compact-value" style="color: {h['color']};">{h['value']:.3f}</div>
                        <div class="compact-delta">{h['regime']}</div>
                        <div class="compact-sub">Confidence: {h['confidence']:.0f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Shannon Entropy
                with col2:
                    e = quant_data['entropy']
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">{e['icon']} MARKET ENTROPY</div>
                        <div class="compact-value" style="color: {e['color']};">{e['score']:.0f}%</div>
                        <div class="compact-delta">{e['regime']}</div>
                        <div class="compact-sub">Risk: {e['risk']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Z-Score
                with col3:
                    z = quant_data['z_score']
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">{z['icon']} Z-SCORE</div>
                        <div class="compact-value" style="color: {z['color']};">{z['value']:.2f}σ</div>
                        <div class="compact-delta">{z['signal']}</div>
                        <div class="compact-sub">{z['action'][:25]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ==========================================
                # ROW 2: BAYESIAN, SHARPE, COMPOSITE
                # ==========================================
                col4, col5, col6 = st.columns(3)
                
                # Bayesian Probability
                with col4:
                    b = quant_data['bayesian']
                    bias_color = "#00ff88" if b['bias'] == 'BULLISH' else "#ff1744" if b['bias'] == 'BEARISH' else "#ffd700"
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">📈 BAYESIAN PROB</div>
                        <div class="compact-value" style="color: {bias_color};">{b['up_probability']:.1f}%</div>
                        <div class="compact-delta">{b['bias']}</div>
                        <div class="compact-sub">Info gain: +{b['info_gain']:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Sharpe Ratio
                with col5:
                    r = quant_data['risk_metrics']
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">📊 SHARPE RATIO</div>
                        <div class="compact-value" style="color: {r['sharpe_color']};">{r['sharpe']:.2f}</div>
                        <div class="compact-delta">{r['sharpe_grade']}</div>
                        <div class="compact-sub">Sortino: {r['sortino']:.2f} | Ω: {r['omega']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Composite Score
                with col6:
                    comp = quant_data['composite_score']
                    comp_color = "#00ff88" if comp >= 70 else "#ffd700" if comp >= 50 else "#ff1744"
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">🎯 COMPOSITE SCORE</div>
                        <div class="compact-value" style="color: {comp_color};">{comp:.0f}</div>
                        <div class="compact-delta">{'Optimal' if comp >= 70 else 'Moderate' if comp >= 50 else 'Poor'}</div>
                        <div class="compact-sub">Higher = Better trading</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ==========================================
                # ROW 3: DRAWDOWN & VAR
                # ==========================================
                st.markdown("---")
                st.markdown(
                    "<div style='font-size: 11px; color: #8892b0; margin-bottom: 10px;'>⚠️ RISK MANAGEMENT METRICS</div>",
                    unsafe_allow_html=True
                )
                
                col7, col8, col9 = st.columns(3)
                
                # Maximum Drawdown
                with col7:
                    d = quant_data['drawdown']
                    dd_color = "#00ff88" if d['max_drawdown'] < 10 else "#ffd700" if d['max_drawdown'] < 20 else "#ff1744"
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">📉 MAX DRAWDOWN</div>
                        <div class="compact-value" style="color: {dd_color};">{d['max_drawdown']:.1f}%</div>
                        <div class="compact-delta">Current: {d['current_drawdown']:.1f}%</div>
                        <div class="compact-sub">Recovery: {d['avg_recovery_days']} days | UI: {d['ulcer_index']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Value at Risk
                with col8:
                    v = quant_data['var']
                    var_color = "#00ff88" if v['var_95'] < 2 else "#ffd700" if v['var_95'] < 4 else "#ff1744"
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">⚠️ VALUE AT RISK (95%)</div>
                        <div class="compact-value" style="color: {var_color};">{v['var_95']:.2f}%</div>
                        <div class="compact-delta">Daily loss: ₹{v['daily_var_rupees']:,}</div>
                        <div class="compact-sub">CVaR: {v['cvar_95']:.2f}% | 99%: {v['var_99']:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Monte Carlo Summary
                with col9:
                    mc = quant_data.get('monte_carlo')
                    if mc:
                        mc_color = "#00ff88" if mc['prob_up'] >= 60 else "#ff1744" if mc['prob_up'] <= 40 else "#ffd700"
                        st.markdown(f"""
                        <div class="compact-box">
                            <div class="compact-label">🎲 MONTE CARLO (5D)</div>
                            <div class="compact-value" style="color: {mc_color};">{mc['prob_up']:.0f}%</div>
                            <div class="compact-delta">{'Bullish' if mc['prob_up'] >= 60 else 'Bearish' if mc['prob_up'] <= 40 else 'Neutral'}</div>
                            <div class="compact-sub">↑+5%: {mc['prob_up_5pct']:.0f}% | ↓-5%: {mc['prob_down_5pct']:.0f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="compact-box">
                            <div class="compact-label">🎲 MONTE CARLO</div>
                            <div class="compact-value" style="color: #8892b0;">Loading...</div>
                            <div class="compact-delta">Need more data</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
                
        except Exception as e:
            # Fall back to basic quant metrics if advanced fails
            st.caption(f"⚠️ Advanced quant models: {str(e)[:50]}...")
        
        # ==========================================
        # BASIC QUANTITATIVE INTELLIGENCE (Fallback)
        # ==========================================
        try:
            quant_metrics = brain.calculate_quantitative_metrics(data, levels)
            
            st.markdown(
                "<div style='font-size: 11px; color: #8892b0; margin-bottom: 10px;'>📊 QUANTITATIVE INTELLIGENCE</div>",
                unsafe_allow_html=True
            )
            
            q_col1, q_col2, q_col3 = st.columns(3)
            
            # Win Probability
            with q_col1:
                win_prob = quant_metrics['win_probability']
                sample_size = quant_metrics['sample_size']
                
                if win_prob >= 70:
                    prob_color = "#00ff88"
                    prob_text = "High Probability"
                elif win_prob >= 60:
                    prob_color = "#ffd700"
                    prob_text = "Good Probability"
                elif win_prob >= 50:
                    prob_color = "#ffa500"
                    prob_text = "Moderate"
                else:
                    prob_color = "#ff1744"
                    prob_text = "Low Probability"
                
                st.markdown(f"""
                <div class="compact-box">
                    <div class="compact-label">🎲 WIN PROBABILITY</div>
                    <div class="compact-value" style="color: {prob_color};">{win_prob}%</div>
                    <div class="compact-delta">{prob_text}</div>
                    <div class="compact-sub">Based on {sample_size} patterns</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Expected Value
            with q_col2:
                exp_value = quant_metrics['expected_value']
                
                if exp_value > 1:
                    ev_color = "#00ff88"
                    ev_text = "Strong Positive"
                elif exp_value > 0:
                    ev_color = "#ffd700"
                    ev_text = "Slightly Positive"
                elif exp_value > -1:
                    ev_color = "#ffa500"
                    ev_text = "Slightly Negative"
                else:
                    ev_color = "#ff1744"
                    ev_text = "Strong Negative"
                
                st.markdown(f"""
                <div class="compact-box">
                    <div class="compact-label">💰 EXPECTED VALUE</div>
                    <div class="compact-value" style="color: {ev_color};">{exp_value:+.2f}%</div>
                    <div class="compact-delta">{ev_text}</div>
                    <div class="compact-sub">Avg return per trade</div>
                </div>
                """, unsafe_allow_html=True)
            
            # AI Verdict
            with q_col3:
                verdict = quant_metrics['verdict']
                message = quant_metrics['message']
                
                if verdict == "STRONG BUY":
                    verdict_color = "#00ff88"
                    verdict_icon = "✅"
                elif verdict == "BUY":
                    verdict_color = "#7cfc00"
                    verdict_icon = "📈"
                elif verdict == "CONSIDER":
                    verdict_color = "#ffd700"
                    verdict_icon = "⚠️"
                elif verdict == "AVOID":
                    verdict_color = "#ff1744"
                    verdict_icon = "❌"
                else:
                    verdict_color = "#8892b0"
                    verdict_icon = "⚡"
                
                short_message = message[:35] + "..." if len(message) > 35 else message
                
                st.markdown(f"""
                <div class="compact-box">
                    <div class="compact-label">{verdict_icon} AI VERDICT</div>
                    <div class="compact-value" style="color: {verdict_color};">{verdict}</div>
                    <div class="compact-delta">{short_message}</div>
                    <div class="compact-sub">Math-based decision</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Add explanation if data is insufficient
            if quant_metrics.get('sample_size', 0) == 0:
                st.caption("📊 *Need more historical data for accurate quantitative analysis. Keep using TORO AI daily!*")
        
        except Exception as e:
            st.caption(f"📊 Quantitative metrics loading: {str(e)[:50]}...")
        
        # ==========================================
        # MONTE CARLO SIMULATION (Detailed)
        # ==========================================
        st.markdown(
            "<div style='font-size: 11px; color: #8892b0; margin-bottom: 10px;'>🎲 MONTE CARLO SIMULATION</div>",
            unsafe_allow_html=True
        )
        
        current_price = data["Close"].iloc[-1]
        target_price = levels.get("target", current_price * 1.05)
        stoploss_price = levels.get("stoploss", current_price * 0.98)
        
        try:
            monte_carlo_results = brain.run_monte_carlo_simulation(
                data,
                current_price,
                target_price,
                stoploss_price
            )
            
            if monte_carlo_results:
                st.markdown(
                    f"<div style='font-size: 10px; color: #64748b; margin-bottom: 10px;'>📊 Based on {monte_carlo_results.get('n_paths', 5000):,} simulated scenarios</div>",
                    unsafe_allow_html=True
                )
                
                mc_col1, mc_col2, mc_col3, mc_col4 = st.columns(4)
                
                with mc_col1:
                    prob_target = monte_carlo_results.get('prob_target', 50)
                    color = "#00ff88" if prob_target >= 60 else "#ffd700" if prob_target >= 50 else "#ff1744"
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">🎯 HIT TARGET</div>
                        <div class="compact-value" style="color: {color};">{prob_target}%</div>
                        <div class="compact-sub">Probability</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with mc_col2:
                    prob_stop = monte_carlo_results.get('prob_stoploss', 50)
                    color_stop = "#ff1744" if prob_stop > 30 else "#ffd700"
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">🛑 HIT STOP LOSS</div>
                        <div class="compact-value" style="color: {color_stop};">{prob_stop}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with mc_col3:
                    exp_return = monte_carlo_results.get('mean_return', 0)
                    return_color = "#00ff88" if exp_return > 0 else "#ff1744"
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">📈 EXPECTED RETURN</div>
                        <div class="compact-value" style="color: {return_color};">{exp_return:+.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with mc_col4:
                    sharpe = monte_carlo_results.get('sharpe', 0)
                    adj_color = "#00ff88" if sharpe > 0.5 else "#ffd700" if sharpe > 0 else "#ff1744"
                    st.markdown(f"""
                    <div class="compact-box">
                        <div class="compact-label">⚡ SHARPE RATIO</div>
                        <div class="compact-value" style="color: {adj_color};">{sharpe:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Best/Worst case scenarios
                if 'price_percentiles' in monte_carlo_results:
                    with st.expander("📊 View Best & Worst Case Scenarios"):
                        bc_col1, bc_col2 = st.columns(2)
                        
                        p95_price = monte_carlo_results['price_percentiles'].get('p95', current_price)
                        p5_price = monte_carlo_results['price_percentiles'].get('p5', current_price)
                        
                        best_return = ((p95_price - current_price) / current_price) * 100
                        worst_return = ((p5_price - current_price) / current_price) * 100
                        
                        with bc_col1:
                            st.metric("🚀 BEST CASE", f"+{best_return:.1f}%")
                            st.caption(f"Target (95th percentile): ₹{p95_price:.2f}")
                        
                        with bc_col2:
                            st.metric("⚠️ WORST CASE", f"{worst_return:.1f}%")
                            st.caption(f"Stop (5th percentile): ₹{p5_price:.2f}")
            
            else:
                st.info("📊 Monte Carlo: Need more data for simulation")
        
        except Exception as e:
            st.info(f"📊 Monte Carlo simulation: {str(e)[:50]}...")