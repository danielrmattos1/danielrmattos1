#!/usr/bin/env python
"""Calcula metas e progresso diário para 99"""

META_DIARIA = 200.0  # R$ 200/dia
META_SEMANAL = 1200.0

def verificar_meta(atual):
    faltando = META_DIARIA - atual
    pct = (atual / META_DIARIA) * 100
    
    if pct >= 100:
        status = "META BATIDA!"
    elif pct >= 80:
        status = "FALTANDO POUCO"
    else:
        status = "EM ANDAMENTO"
    
    return f"{status} - Faltam R$ {faltando:.2f} ({pct:.0f}%)"

if __name__ == "__main__":
    import sys
    ganho_hoje = float(sys.argv[1]) if len(sys.argv) > 1 else 0
    print(verificar_meta(ganho_hoje))
