# src/plots.py
from __future__ import annotations
import os
import pandas as pd
import matplotlib.pyplot as plt

def _ensure_dir(path: str | None):
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)

def plot_cumulative(cum_df: pd.DataFrame, title: str = "Performance cumulée", save_as: str | None = None):
    ax = cum_df.plot(figsize=(10, 5), title=title)
    ax.set_ylabel("Croissance (base = 1.0)")
    ax.grid(True, alpha=0.3)
    if save_as:
        _ensure_dir(save_as)
        plt.savefig(save_as, dpi=150, bbox_inches="tight")
    plt.show()

def plot_hist(returns: pd.Series, bins: int = 50, title: str = "Histogramme des rendements", save_as: str | None = None):
    ax = returns.hist(bins=bins, figsize=(8, 4))
    ax.set_title(title)
    ax.set_xlabel("Rendements quotidiens")
    ax.set_ylabel("Fréquence")
    if save_as:
        _ensure_dir(save_as)
        plt.savefig(save_as, dpi=150, bbox_inches="tight")
    plt.show()

def plot_drawdown(returns: pd.Series, title: str = "Courbe de drawdown", save_as: str | None = None) -> pd.Series:
    growth = (1.0 + returns).cumprod()
    running_max = growth.cummax()
    drawdown = growth / running_max - 1.0
    ax = drawdown.plot(figsize=(10, 5), title=title)
    ax.set_ylabel("Drawdown")
    ax.grid(True, alpha=0.3)
    if save_as:
        _ensure_dir(save_as)
        plt.savefig(save_as, dpi=150, bbox_inches="tight")
    plt.show()
    return drawdown
