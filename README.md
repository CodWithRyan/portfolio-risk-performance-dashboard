# Portfolio Risk & Performance Dashboard

## Objectif
Analyser la performance et le risque d’un portefeuille multi-actifs (actions/ETF/devises) avec Python.

## Données
- Source: Yahoo Finance (via `yfinance`)
- Période: [ex: 5 ans]
- Tickers: [ex: SPY, AAPL, MSFT, TSLA, EURUSD=X]

## Indicateurs (V1)
- Rendement cumulé
- Volatilité annualisée
- Ratio de Sharpe (Rf = 0%)
- Drawdown & Max Drawdown

## Visualisations (V1)
1. Performance cumulée (portefeuille vs benchmark)
2. Histogramme des rendements quotidiens
3. Courbe de drawdown

## Architecture

.
├── data/         # (non versionné)
├── notebooks/
│   └── PortfolioDashboard.ipynb
├── src/
│   ├── data.py
│   ├── metrics.py
│   └── plots.py
├── outputs/      # (non versionné)
├── requirements.txt
└── README.md

## Critères de réussite (V1)
- Notebook exécutable sur clone vierge
- 3 graphes générés
- Tableau récapitulatif des métriques produit

## Références théoriques (Hull, 11e éd. fr.)
- Ch. 14–15 (fondements vols)
- Ch. 22 (VaR)
- Ch. 20 : Courbes de volatilité
- Ch. 23 (vols/corrélations)

## Spécification V1

**Indicateurs**  
- Rendement cumulé  
- Volatilité annualisée  
- Ratio de Sharpe (Rf = 0%)  
- Drawdown & Max Drawdown  

**Graphes**  
- Performance cumulée (portefeuille vs benchmark)  
- Histogramme des rendements quotidiens  
- Courbe de drawdown  

**Livrables**  
- Notebook exécutable  
- 3 graphes sauvegardés dans `/outputs`  
- Tableau des métriques (DataFrame) affiché dans le notebook  
- (Optionnel) Export Excel des résultats  

**Critères de réussite**  
- Le projet doit tourner de bout en bout sur un clone vierge (juste `git clone`, `pip install -r requirements.txt`, et exécution du notebook).
