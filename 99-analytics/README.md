# 99 Analytics

Dashboard e automações para motorista parceiro.

## Arquivos
- `dashboard.py` - Calcula métricas (corridas, km, ganhos, eficiência)
- `metas.py` - Verifica progresso diário
- `templates.csv` - Template para registro de corridas

## Uso
```bash
# Ver métricas atuais
python 99-analytics/dashboard.py

# Verificar meta diária
python 99-analytics/metas.py 150.50
```

## Métricas Calculadas
- Total de corridas (99 vs Uber)
- Quilometragem total
- Ganho total e por km
- Eficiência (R$/km)

## Dashboard Simples
Abra `99-analytics/dashboard.html` no navegador para visualização.
