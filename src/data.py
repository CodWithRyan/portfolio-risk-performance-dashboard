# src/data.py
from __future__ import annotations

import os
from typing import Sequence
import pandas as pd
import yfinance as yf


def get_prices(
    tickers: Sequence[str] | str,
    start: str,
    end: str,
    *,
    min_obs: int = 252 * 2,
    cache_csv: str | None = None,
    auto_adjust: bool = True,
) -> pd.DataFrame:
    """
    Télécharge des PRIX AJUSTÉS (Yahoo Finance via yfinance), nettoie et retourne un DataFrame prêt
    pour les calculs de rendements et de risque.

    Args:
        tickers: symbole ou liste de symboles (ex: "AAPL" ou ["AAPL","MSFT","SPY"])
        start: date de début "YYYY-MM-DD"
        end: date de fin "YYYY-MM-DD"
        min_obs: nb minimal d'observations exigées (≈2 ans ouvrés par défaut)
        cache_csv: chemin CSV pour sauvegarder les prix (optionnel)
        auto_adjust: si True (défaut), yfinance applique les ajustements et la colonne utile est "Close"

    Returns:
        DataFrame (index = dates, colonnes = tickers, dtype float64)

    Raises:
        ValueError si entrées invalides / pas de données / historique trop court / tickers manquants.
    """
    # --- Normalisation des tickers
    if isinstance(tickers, str):
        tickers = [tickers]
    tickers = [t.strip().upper() for t in tickers if t and t.strip()]
    if not tickers:
        raise ValueError("`tickers` doit contenir au moins un symbole non vide.")

    # --- Téléchargement
    try:
        raw = yf.download(
            tickers,
            start=start,
            end=end,
            progress=False,
            auto_adjust=auto_adjust,
        )
    except Exception as e:
        raise RuntimeError(f"Échec du téléchargement yfinance: {e}") from e

    if isinstance(raw, pd.DataFrame) and raw.empty:
        raise ValueError("Aucune donnée téléchargée. Vérifie tickers/dates/connexion.")

    # --- Sélection du champ prix selon la structure renvoyée par yfinance
    def _select_price(df: pd.DataFrame) -> pd.DataFrame | pd.Series:
        if isinstance(df.columns, pd.MultiIndex):
            lv0 = df.columns.get_level_values(0)
            if "Adj Close" in lv0:
                return df["Adj Close"]
            if "Close" in lv0:              # auto_adjust=True → prix ajustés sous "Close"
                return df["Close"]
            raise ValueError(f"Colonnes de prix absentes (vu: {set(lv0)})")
        else:
            if "Adj Close" in df.columns:
                return df["Adj Close"]
            if "Close" in df.columns:
                return df["Close"]
            raise ValueError(f"Colonnes de prix absentes (vu: {list(df.columns)})")

    adj = _select_price(raw)

    # --- Si un seul ticker, forcer DataFrame
    if isinstance(adj, pd.Series):
        adj = adj.to_frame(name=tickers[0])

    # --- Nettoyage & garanties de forme
    adj = adj.sort_index()
    if adj.index.has_duplicates:
        adj = adj[~adj.index.duplicated(keep="last")]
    adj = adj.ffill().dropna(how="any")
    adj = adj.astype("float64")

    # --- Vérifier que tous les tickers demandés sont là
    missing = [t for t in tickers if t not in adj.columns]
    if missing:
        raise ValueError(f"Tickers absents des données: {missing}")

    # --- Historique minimal
    if len(adj) < min_obs:
        raise ValueError(
            f"Historique insuffisant ({len(adj)} lignes). "
            f"Exige au moins {min_obs} observations (paramètre `min_obs`)."
        )

    # --- Cache optionnel
    if cache_csv:
        os.makedirs(os.path.dirname(cache_csv), exist_ok=True)
        adj.to_csv(cache_csv, index=True)

    return adj

