# wc2026-bets Copilot

Sistema automatizado de identificação de value bets para Copa 2026.

## Componentes

### analyzers/
- `odds_extractor.py` - Extrai odds de screenshots via OCR
- `groundtruth_api.py` - Consulta GROUNDTRUTH local (server.py)
- `value_calculator.py` - Calcula EV e tier

### scripts/
- `analyze_daily.py` - Roda análise diária
- `export_valuebets.py` - Exporta CSV para controle

### data/
- `screenshots/` - Imagens de odds (Pinnacle, KTO)
- `output/` - CSVs gerados

## Uso

```bash
# Analisar screenshots do dia
python analyzers/analyze_daily.py

# Resultado: owl_valuebets_HHMM.csv
```

## Workflow

1. Screenshots em `Downloads/` → `data/screenshots/`
2. OCR extrai odds + jogos
3. Compara com GROUNDTRUTH (odd justa)
4. Calcula EV = (odd_fornecida / odd_justa - 1) * 100
5. Classifica tier: S(>=5%), A(3-5%), B(2.5-3%)
6. Exporta CSV