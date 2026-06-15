#!/usr/bin/env python
# 99 Analytics - Dashboard simples
import csv
from datetime import datetime

def calcular_metricas(arquivo_csv):
    """Calcula métricas básicas das corridas"""
    total_corridas = 0
    total_km = 0
    total_ganho = 0
    total_corridas_99 = 0
    total_corridas_uber = 0
    
    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                km = float(row.get('km', 0))
                ganho = float(row.get('ganho', 0))
                app = row.get('app', '')
                
                total_corridas += 1
                total_km += km
                total_ganho += ganho
                
                if '99' in app.lower():
                    total_corridas_99 += 1
                elif 'uber' in app.lower():
                    total_corridas_uber += 1
    except FileNotFoundError:
        pass
    
    eficiencia = total_ganho / total_km if total_km > 0 else 0
    
    return {
        'corridas': total_corridas,
        'km': total_km,
        'ganho': total_ganho,
        'eficiencia': eficiencia,
        'corridas_99': total_corridas_99,
        'corridas_uber': total_corridas_uber
    }

if __name__ == "__main__":
    m = calcular_metricas("data/corridas.csv")
    print(f"Total: {m['corridas']} corridas | {m['km']:.1f} km | R$ {m['ganho']:.2f} | R$ {m['eficiencia']:.2f}/km")
    print(f"99: {m['corridas_99']} | Uber: {m['corridas_uber']}")