# finc-market-cap-snapshot

Insumo público do Black-Litterman do [FinC PMS](https://github.com/MatheusVSX/finc-pms) (repositório privado) — capitalização de mercado (Financial Modeling Prep) dos ativos americanos cobertos, publicada semanalmente por automação.

- `tickers.json` — lista curada de tickers, editada pelo desenvolvedor via a tela "Ferramentas Dev" do app.
- `market_caps.json` — gerado toda segunda-feira pelo workflow (`.github/workflows/snapshot.yml`), lido por qualquer instalação do FinC PMS via GET anônimo (sem chave, sem cadastro).

Defasagem de até uma semana é aceitável aqui: preço, retorno e volatilidade continuam sempre recalculados na hora pelo app; só o peso relativo entre ativos usado no cálculo do retorno de equilíbrio do Black-Litterman vem deste snapshot — uma técnica desenhada justamente para usar uma referência estável, não um sinal de curto prazo.
