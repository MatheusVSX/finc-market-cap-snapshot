#!/usr/bin/env python3
"""Gera market_caps.json a partir de tickers.json, usando a Financial
Modeling Prep (endpoint /stable/profile, campo marketCap -- verificado
ao vivo na sessão que criou este repositório; o endpoint
/api/v3/market-capitalization está descontinuado, "Legacy Endpoint").

Roda dentro do workflow semanal do GitHub Actions (.github/workflows/
snapshot.yml) -- a chave FMP vem de FMP_API_KEY (GitHub Secret), nunca
hardcoded. Ticker que falhar (não encontrado na FMP, rede instável) é
pulado com um aviso, não derruba a publicação inteira.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("FMP_API_KEY")
if not API_KEY:
    print("FMP_API_KEY não definida", file=sys.stderr)
    sys.exit(1)

with open("tickers.json", encoding="utf-8") as f:
    tickers = json.load(f)["tickers"]

caps = {}
for ticker in tickers:
    url = f"https://financialmodelingprep.com/stable/profile?symbol={ticker}&apikey={API_KEY}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            body = json.load(resp)
        if not body:
            print(f"{ticker}: não encontrado na FMP", file=sys.stderr)
            continue
        caps[ticker] = body[0]["marketCap"]
        print(f"{ticker}: US$ {caps[ticker]:,.2f}")
    except Exception as e:  # noqa: BLE001 -- um ticker ruim não derruba os outros
        print(f"{ticker}: falhou -- {e}", file=sys.stderr)

snapshot = {"gerado_em": datetime.now(timezone.utc).isoformat(), "caps": caps}
with open("market_caps.json", "w", encoding="utf-8") as f:
    json.dump(snapshot, f, indent=2, ensure_ascii=False)

print(f"\n{len(caps)}/{len(tickers)} tickers publicados em market_caps.json")
