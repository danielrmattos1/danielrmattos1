# HERMES — MONITOR COPA 2026 + TELEGRAM + CRON

## Configuração global

```python
ODDS_API_KEY   = "b3929018479517092f9f7e9437994705"
TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"       # @BotFather
TELEGRAM_CHAT  = "SEU_CHAT_ID_AQUI"    # @userinfobot
SHARP_BOOKS    = ["pinnacle", "betfair"]

SINAIS = [
    {
        "jogo": "Brasil vs Marrocos", "home": "Brazil", "away": "Morocco",
        "sport": "soccer_fifa_world_cup", "mercado": "Empate",
        "data_br": "13/06 19h", "floor": 3.89, "odd_alvo": 4.00, "kelly": 0.0096,
    },
    {
        "jogo": "França vs Senegal", "home": "France", "away": "Senegal",
        "sport": "soccer_fifa_world_cup", "mercado": "Empate",
        "data_br": "16/06 16h", "floor": 4.10, "odd_alvo": 4.90, "kelly": 0.0157,
    },
]
```

---

## Tarefa 1 — Criar /root/monitor.py

O script deve:

1. Buscar odds via The Odds API (regiões `eu` + `uk`)
2. Calcular odd justa com Pinnacle (sem margem)
3. Determinar status de cada sinal:
   - `🟢 ENTRAR` → odd mercado ≥ odd_alvo
   - `🟡 MONITORAR` → odd entre floor e alvo
   - `🔴 CANCELAR` → odd abaixo do floor
4. Detectar mudança de status vs execução anterior
5. Enviar mensagem Telegram formatada
6. Salvar histórico em `/root/odds_history.jsonl`

### Lógica de cálculo

```python
# Probabilidade Pinnacle sem margem
raw   = {o["name"]: 1/o["price"] for o in outcomes}
total = sum(raw.values())
probs = {k: v/total for k, v in raw.items()}
odd_justa = round(1 / probs["Draw"], 2)

# EV
ev = (probs["Draw"] * odd_mercado) - 1
```

### Formato da mensagem Telegram

```
🤖 HERMES — MONITOR COPA 2026
📅 08/06 13:00 (Brasília)
━━━━━━━━━━━━━━━━━━━━━━━━

⚽ Brasil vs Marrocos | 13/06 19h
📊 Odd justa:    3.89  (Pinnacle)
📈 Melhor odd:   4.00  (Betfair)
🎯 Alvo: 4.00  |  Floor: 3.89
STATUS: 🟢 ENTRAR

✅ Abra KTO ou Bet365
   Se Empate ≥ 3.89 → APOSTAR
   Stake: 0.96% da banca
   Ex: R$1.000 → R$9,60

─────────────────────────────
⚽ França vs Senegal | 16/06 16h
...
━━━━━━━━━━━━━━━━━━━━━━━━
_Hermes Agent • Apenas educacional_
```

### Alerta de mudança de status (extra)

Se o status mudar entre execuções, enviar alerta adicional:

```
🚨 MUDANÇA — Brasil vs Marrocos
Antes:  🟡 MONITORAR (odd 3.95)
Agora:  🟢 ENTRAR    (odd 4.05)
✅ VERIFIQUE KTO/BET365 AGORA!
```

---

## Tarefa 2 — Instalar dependências

```bash
pip install requests python-telegram-bot --break-system-packages
```

---

## Tarefa 3 — Configurar cron job

```bash
# Abrir crontab
crontab -e

# Adicionar linha (executa todo dia às 13h Brasília = 16h UTC)
0 16 * * * /usr/bin/python3 /root/monitor.py >> /root/monitor.log 2>&1
```

Verificar se foi criado:
```bash
crontab -l
```

---

## Tarefa 4 — Testar agora

```bash
python3 /root/monitor.py
```

Confirmar:
- Telegram recebeu a mensagem
- `/root/odds_history.jsonl` foi criado
- Log sem erros

---

## Regras permanentes

- Sharp book = apenas para calcular EV, nunca para apostar
- Casas de entrada = KTO e Bet365 (verificação manual)
- Múltiplas = proibido — apenas apostas simples separadas
- Kelly fracionado = metade do Kelly em soft books (KTO, Bet365)
- Não enviar Telegram se status for igual ao anterior (sem mudança)
