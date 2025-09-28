# src/metrics.py
from __future__ import annotations
import numpy as np
import pandas as pd

TRADING_DAYS = 252

def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Rendements quotidiens simples pour chaque ticker.
    """
    rets = prices.pct_change().dropna(how="any")
    if rets.isna().any().any():
        raise ValueError("NaN présents après pct_change(); vérifie les prix.")
    return rets

def equal_weighted_portfolio(returns: pd.DataFrame) -> pd.Series:
    """
    Portefeuille équipondéré (moyenne des colonnes ligne par ligne).
    """
    if returns.empty:
        raise ValueError("returns est vide.")
    return returns.mean(axis=1)

def cumulative_growth(returns: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    """
    Courbe de croissance (base 1.0) = (1+r).cumprod().
    """
    return (1.0 + returns).cumprod()

def cumulative_return(returns: pd.Series) -> float:
    """
    Rendement cumulé sur la période.
    """
    return float((1.0 + returns).prod() - 1.0)

def annualized_volatility(returns: pd.Series, periods: int = TRADING_DAYS) -> float:
    """
    Écart-type quotidien annualisé.
    """
    return float(returns.std() * np.sqrt(periods))

def sharpe_ratio(returns: pd.Series, rf_annual: float = 0.0, periods: int = TRADING_DAYS) -> float:
    """
    Sharpe basé sur rendements quotidiens. rf_annual en taux annuel (ex: 0.02 pour 2%).
    """
    excess_daily = returns - rf_annual / periods
    return float((excess_daily.mean() / excess_daily.std()) * np.sqrt(periods))

def max_drawdown(returns: pd.Series) -> float:
    """
    Pire creux historique sur la période (valeur négative).
    """
    growth = cumulative_growth(returns)
    running_max = growth.cummax()
    drawdown = growth / running_max - 1.0
    return float(drawdown.min())

def summarize_metrics(returns_df: pd.DataFrame, portfolio: pd.Series, rf_annual: float = 0.0) -> pd.DataFrame:
    """
    Tableau récapitulatif pour chaque actif + PORTFOLIO.
    """
    def _one(s: pd.Series) -> pd.Series:
        return pd.Series({
            "CumulativeReturn": cumulative_return(s),
            "AnnVol":          annualized_volatility(s),
            "Sharpe":          sharpe_ratio(s, rf_annual=rf_annual),
            "MaxDrawdown":     max_drawdown(s),
        })

    table = returns_df.apply(_one, axis=0).T
    table.loc["PORTFOLIO"] = _one(portfolio)
    return table
