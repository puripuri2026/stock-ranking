from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import pandas as pd
import yfinance as yf

def read_stocks(path):
    if not path.exists():
        raise FileNotFoundError(f"銘柄リストが見つかりません: {path}")
    stocks = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        code = parts[0].strip().upper()
        name = parts[1].strip() if len(parts) > 1 else code
        if not re.fullmatch(r"[0-9A-Z]{4,5}", code):
            print(f"警告: {line_no}行目を読み飛ばします: {raw}", file=sys.stderr)
            continue
        stocks.append({"code": code, "name": name, "ticker": f"{code}.T"})
    if not stocks:
        raise ValueError("stocks.txt に有効な銘柄がありません。例: 3901 マークラインズ")
    return stocks

def download_one(stock):
    ticker = stock["ticker"]
    print(f"株価取得中: {ticker} ({stock['name']})")
    frame = yf.download(ticker, period="10y", interval="1d", auto_adjust=False, progress=False, threads=False)
    if frame is None or frame.empty:
        print(f"警告: データを取得できませんでした: {ticker}", file=sys.stderr)
        return {**stock, "data": [], "error": "株価データを取得できませんでした"}
    if isinstance(frame.columns, pd.MultiIndex):
        level0 = set(map(str, frame.columns.get_level_values(0)))
        frame.columns = frame.columns.get_level_values(0) if {"Open","High","Low","Close"}.issubset(level0) else frame.columns.get_level_values(-1)
    required = ["Open", "High", "Low", "Close"]
    if not all(c in frame.columns for c in required):
        return {**stock, "data": [], "error": "OHLC列がありません"}
    frame = frame[required].dropna(subset=required)
    rows = []
    for timestamp, row in frame.iterrows():
        try:
            rows.append({
                "time": pd.Timestamp(timestamp).date().isoformat(),
                "open": round(float(row["Open"]), 4),
                "high": round(float(row["High"]), 4),
                "low": round(float(row["Low"]), 4),
                "close": round(float(row["Close"]), 4),
            })
        except (TypeError, ValueError):
            continue
    return {**stock, "data": rows, "error": None if rows else "株価データがありません"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="stocks.txt")
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stocks = read_stocks(Path(args.input))
    results = []
    for stock in stocks:
        try:
            results.append(download_one(stock))
        except Exception as exc:
            print(f"警告: {stock['ticker']} の処理中にエラー: {exc}", file=sys.stderr)
            results.append({**stock, "data": [], "error": str(exc)})
    successful = sum(bool(x["data"]) for x in results)
    payload = {
        "generatedAt": pd.Timestamp.now(tz="Asia/Tokyo").isoformat(),
        "source": "Yahoo Finance via yfinance",
        "historyYears": 10,
        "stocks": results,
    }
    out = output_dir / "stock_data.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"出力: {out}（{successful}/{len(results)}銘柄で取得）")
    if successful == 0:
        raise RuntimeError("全銘柄の株価データを取得できませんでした。")

if __name__ == "__main__":
    main()
