# wc2026-bets

Repositório com dois sistemas independentes.

## 📊 99 Analytics (Corridas)
Sistema de métricas para motorista parceiro 99/Uber.

**Path:** `./99-analytics/`
- `dashboard.py` - Métricas (corridas, km, R$/km)
- `metas.py` - Meta diária/semanal
- `templates.csv` - Registro padrão
- `dashboard.html` - Visualização

```bash
python 99-analytics/dashboard.py        # Métricas
python 99-analytics/metas.py 150.50    # Ver meta
```

## ⚽ Value Bets (Copa 2026)
Sistema de value betting para a Copa do Mundo 2026.

**Path:** `./`
- `controle-banca.html` - Interface registro apostas
- `owl_controle_copa2026.*` - Histórico
- `index.html` - GROUNDTRUTH prediction engine
- `workflow.md` - Pipeline Hermes

## 📱 Telegram Bot
- Gateway rodando (08:00 diário)
- TELEGRAM_BOT_TOKEN configurado
- THE_ODDS_API_KEY validada

---

*Dois projetos, workflows separados.*