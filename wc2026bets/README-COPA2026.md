# Copa 2026 - Value Betting System

Sistema pessoal de análise e controle de value bets para a Copa do Mundo 2026.

## Workflow Diário

1. **Manhã** - Prints de odds do Pinnacle e KTO em `C:/Users/danie/Downloads/`
2. **Análise OWL** - Comparação: KTO vs Pinnacle + GROUNDTRUTH
3. **Value identificado** - Entry registrada no controle de banca

## Estrutura do Projeto

```
copa-2026-betting/
├── controle-banca.html      # Interface web para registrar apostas
├── owl_controle_copa2026.html  # Versão OWL com dados iniciais
├── owl_controle_copa2026.csv    # Histórico de apostas (CSV)
├── hermes_copa2026_2026-06-13.csv  # Planilha de value bets
├── workflow.md            # Documentação do pipeline Hermes
├── monitor-telegram.md    # Configuração do monitor Telegram
├── index.html             # GROUNDTRUTH - Motor de previsões
├── server.py              # Backend opcional para results
├── README.md              # Documentação GROUNDTRUTH
└── METHODOLOGY.md         # Metodologia Elo+Poisson
```

## Tiers de Value

| Tier | EV Range | Critério |
|------|----------|----------|
| S | ≥5% | Alta confiança |
| A | 3-5% | Média confiança |
| B | 2.5-3% | Baixa confiança |

## Cross-check Pinnacle vs KTO

- **GROUNDTRUTH** fornece odd justa (Pinnacle sem margem)
- **KTO** é a casa de entrada para value bets
- Validação: KTO/Pinnacle + GROUNDTRUTH = alta confiança

## API The Odds

- Chave configurada: THE_ODDS_API_KEY em `~/.hermes/.env`
- Limite: 500 requests/mês (plano free)
- Uso: screenshots primeiro, API apenas para cross-check

## Telegram Bot

- Token: TELEGRAM_BOT_TOKEN (arquivo `.env`)
- Cron job: "Daily Briefing - Tatuapé" (08:00 diário)
- Gateway rodando via polling

## Histórico (14/06/2026)

| Data | Jogo | Mercado | Casa | Odd | Stake | EV | Resultado |
|------|------|---------|------|-----|-------|-----|-----------|
| 2026-06-07 | Brasil vs Marrocos | Empate | KTO | 3.95 | 50.00 | 50.1% | WIN (+147.50) |
| 2026-06-12 | Canadá vs Bósnia | Bósnia | KTO | 4.75 | 0.50 | 9.7% | LOSS (-0.50) |
| 2026-06-12 | EUA vs Paraguai | EUA | KTO | 2.12 | 0.50 | 7.1% | WIN (+0.56) |
| 2026-06-13 | Austrália vs Turquia | Austrália | KTO | 6.00 | 0.50 | 10.5% | CASHOUT (0.68 / 1.18) |
| 2026-06-13 | Arábia Saudita vs Uruguai | Arábia Saudita | KTO | 9.00 | 0.50 | - | CASHOUT (0.00 / 0.50) |

Total: 5 apostas, 2 wins, 1 loss, 2 cashouts | Banca atual: R$50.00

---

*Este é um repositório pessoal de estudos e não constitui aconselhamento de apostas.*