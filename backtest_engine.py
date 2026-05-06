# backtest_engine.py - Complete Version with Visualizer

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class BacktestVisualizer:
    """Create professional visualizations for backtest results"""
    
    @staticmethod
    def create_equity_chart(equity_curve, trades_df, initial_capital):
        """Create interactive equity curve chart"""
        
        if equity_curve.empty:
            return None
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            row_heights=[0.7, 0.3],
            subplot_titles=("Portfolio Equity", "Drawdown")
        )
        
        # Equity curve
        fig.add_trace(
            go.Scatter(
                x=equity_curve['date'],
                y=equity_curve['equity'],
                mode='lines',
                name='Portfolio Value',
                line=dict(color='#00ffff', width=2),
                fill='tozeroy',
                fillcolor='rgba(0,255,255,0.1)'
            ),
            row=1, col=1
        )
        
        # Drawdown calculation
        equity_values = equity_curve['equity'].values
        peak = np.maximum.accumulate(equity_values)
        drawdown = (equity_values - peak) / peak * 100
        
        fig.add_trace(
            go.Scatter(
                x=equity_curve['date'],
                y=drawdown,
                mode='lines',
                name='Drawdown %',
                line=dict(color='#ff1744', width=1.5),
                fill='tozeroy',
                fillcolor='rgba(255,23,68,0.2)'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            template='plotly_dark',
            height=500,
            showlegend=True,
            hovermode='x unified'
        )
        
        fig.update_yaxes(title_text="Portfolio Value (₹)", row=1, col=1)
        fig.update_yaxes(title_text="Drawdown (%)", row=2, col=1)
        
        return fig


class BacktestEngine:
    """Professional Backtesting Engine - CORRECTED VERSION"""
    
    def __init__(self, initial_capital=100000, commission=0.0005, slippage=0.001):
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.trades = []
        self.daily_equity = []
        
    def calculate_max_drawdown(self, equity_values):
        """Calculate maximum drawdown from equity curve"""
        if not equity_values:
            return 0
        
        peak = equity_values[0]
        max_drawdown = 0
        
        for value in equity_values:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        return round(max_drawdown, 2)
    
    def calculate_sharpe_ratio(self, daily_returns, risk_free_rate=0.06):
        """Calculate proper Sharpe Ratio"""
        if len(daily_returns) < 2:
            return 0
        
        returns_array = np.array(daily_returns)
        avg_daily_return = np.mean(returns_array)
        annual_return = avg_daily_return * 252
        daily_vol = np.std(returns_array)
        annual_vol = daily_vol * np.sqrt(252)
        
        if annual_vol == 0:
            return 0
        
        sharpe = (annual_return - risk_free_rate) / annual_vol
        return round(sharpe, 2)
    
    def run_backtest(self, df, levels_calculator, signal_generator):
        """Run complete backtest"""
        
        if df.empty or len(df) < 50:
            return self._empty_results("Insufficient data")
        
        capital = self.initial_capital
        in_position = False
        entry_price = 0
        position_size = 0
        entry_date = None
        stop_loss = 0
        target = 0
        
        self.trades = []
        self.daily_equity = []
        daily_returns = []
        
        for i in range(50, len(df)):
            current_date = df.index[i]
            current_price = df['Close'].iloc[i]
            current_data = df.iloc[:i+1].copy()
            
            levels = levels_calculator(current_data)
            signal = signal_generator(current_data, levels)
            
            if in_position:
                current_value = capital + (position_size * (current_price - entry_price))
            else:
                current_value = capital
            
            self.daily_equity.append(current_value)
            
            if i > 50 and len(self.daily_equity) > 1:
                daily_return = (current_value - self.daily_equity[-2]) / self.daily_equity[-2]
                daily_returns.append(daily_return)
            
            # Entry logic
            if signal == 1 and not in_position and levels:
                position_value = min(capital * 0.2, self.initial_capital * 0.2)
                position_size = position_value / current_price
                entry_price = current_price * (1 + self.slippage)
                entry_date = current_date
                stop_loss = levels.get('stoploss', current_price * 0.97)
                target = levels.get('target', current_price * 1.05)
                in_position = True
                
            # Exit logic
            elif in_position:
                exit_signal = False
                exit_reason = ""
                exit_price = current_price
                
                if current_price <= stop_loss:
                    exit_signal = True
                    exit_reason = "Stop Loss"
                    exit_price = current_price * (1 - self.slippage)
                elif current_price >= target:
                    exit_signal = True
                    exit_reason = "Target"
                    exit_price = current_price * (1 - self.slippage)
                elif signal == -1:
                    exit_signal = True
                    exit_reason = "Sell Signal"
                    exit_price = current_price * (1 - self.slippage)
                
                if exit_signal:
                    trade_return = (exit_price - entry_price) / entry_price
                    pnl = position_size * (exit_price - entry_price)
                    pnl = pnl - (position_size * entry_price * self.commission)
                    pnl = pnl - (position_size * exit_price * self.commission)
                    
                    self.trades.append({
                        'entry_date': entry_date,
                        'exit_date': current_date,
                        'entry_price': round(entry_price, 2),
                        'exit_price': round(exit_price, 2),
                        'return_pct': round(trade_return * 100, 2),
                        'pnl': round(pnl, 2),
                        'reason': exit_reason,
                        'days_held': (current_date - entry_date).days
                    })
                    
                    capital += pnl
                    in_position = False
                    position_size = 0
        
        metrics = self._calculate_metrics(daily_returns)
        max_drawdown = self.calculate_max_drawdown(self.daily_equity)
        metrics['max_drawdown'] = max_drawdown
        
        if daily_returns:
            metrics['sharpe_ratio'] = self.calculate_sharpe_ratio(daily_returns)
        
        final_capital = capital
        total_return = ((final_capital - self.initial_capital) / self.initial_capital) * 100
        
        return {
            'metrics': metrics,
            'trades': pd.DataFrame(self.trades),
            'equity_curve': pd.DataFrame({'date': df.index[50:], 'equity': self.daily_equity}),
            'final_capital': round(final_capital, 2),
            'total_return': round(total_return, 2),
            'max_drawdown': max_drawdown,
            'sharpe_ratio': metrics.get('sharpe_ratio', 0)
        }
    
    def _calculate_metrics(self, daily_returns):
        if not self.trades:
            return self._empty_metrics()
        
        trades_df = pd.DataFrame(self.trades)
        total_trades = len(trades_df)
        winning_trades = trades_df[trades_df['return_pct'] > 0]
        losing_trades = trades_df[trades_df['return_pct'] <= 0]
        
        win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0
        avg_return = trades_df['return_pct'].mean()
        avg_win = winning_trades['return_pct'].mean() if len(winning_trades) > 0 else 0
        avg_loss = losing_trades['return_pct'].mean() if len(losing_trades) > 0 else 0
        
        total_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
        total_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0
        profit_factor = total_profit / total_loss if total_loss > 0 else total_profit
        
        largest_win = trades_df['return_pct'].max() if len(trades_df) > 0 else 0
        largest_loss = trades_df['return_pct'].min() if len(trades_df) > 0 else 0
        expectancy = (win_rate/100 * avg_win) - ((100-win_rate)/100 * abs(avg_loss)) if avg_loss != 0 else avg_win
        avg_days_held = trades_df['days_held'].mean() if 'days_held' in trades_df.columns else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': round(win_rate, 2),
            'avg_return_pct': round(avg_return, 2),
            'avg_win_pct': round(avg_win, 2),
            'avg_loss_pct': round(avg_loss, 2),
            'total_profit': round(total_profit, 2),
            'total_loss': round(total_loss, 2),
            'profit_factor': round(profit_factor, 2),
            'largest_win_pct': round(largest_win, 2),
            'largest_loss_pct': round(largest_loss, 2),
            'avg_days_held': round(avg_days_held, 1),
            'expectancy_pct': round(expectancy, 2),
            'sharpe_ratio': 0,
            'max_drawdown': 0
        }
    
    def _empty_metrics(self):
        return {
            'total_trades': 0, 'winning_trades': 0, 'losing_trades': 0,
            'win_rate': 0, 'avg_return_pct': 0, 'avg_win_pct': 0,
            'avg_loss_pct': 0, 'total_profit': 0, 'total_loss': 0,
            'profit_factor': 0, 'largest_win_pct': 0, 'largest_loss_pct': 0,
            'avg_days_held': 0, 'expectancy_pct': 0, 'sharpe_ratio': 0,
            'max_drawdown': 0
        }
    
    def _empty_results(self, message):
        return {
            'metrics': self._empty_metrics(),
            'trades': pd.DataFrame(),
            'equity_curve': pd.DataFrame(),
            'final_capital': self.initial_capital,
            'total_return': 0,
            'max_drawdown': 0,
            'sharpe_ratio': 0,
            'message': message
        }