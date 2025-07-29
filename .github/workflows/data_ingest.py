#!/usr/bin/env python3
"""
Download the last 60 daily bars for every ticker in config.yaml
and save them in trading-data/bars/<TICKER>.csv
"""

import os
import datetime as dt
import yfinance as yf
import pandas as pd
from pathlib import Path
import yaml

# ---------- config ----------
CONFIG = {
    "universe": ["SPY", "QQQ"],
    "lookback_days": 60,
    "data_dir": Path("trading-data") / "bars",
}

# allow override from config.yaml if present
cfg_file = Path("config.yaml")
if cfg_file.exists():
    CONFIG.update(yaml.safe_load(cfg_file.read_text()))

CONFIG["data_dir"].mkdir(parents=True, exist_ok=True)
# ----------------------------

def fetch(ticker: str) -> pd.DataFrame:
    end = dt.date.today()
    start = end - dt.timedelta(days=CONFIG["lookback_days"])
    return yf.download(ticker, start=start, end=end, progress=False)

def main() -> None:
    for tkr in CONFIG["universe"]:
        df = fetch(tkr)
        out = CONFIG["data_dir"] / f"{tkr}.csv"
        df.to_csv(out)
        print(f"🟢  saved {tkr} → {out}")

if __name__ == "__main__":
    main()
