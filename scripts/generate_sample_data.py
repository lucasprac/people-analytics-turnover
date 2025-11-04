#!/usr/bin/env python3
"""
Processamento de dados sintéticos para demonstração
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_sample_data():
    """Gera dados sintéticos para demonstração"""
    np.random.seed(42)
    n_active = 300  # colaboradores ativos
    n_exit = 50     # ex-colaboradores
    
    # Colaboradores ativos (clima)
    active_data = []
    for i in range(n_active):
        row = {
            'response_id': f'clima_{i}',
            'form_type': 'clima',
            'employee_id': f'emp_{i}',
            'sede': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Brasília', 'Recife']),
            'cargo': np.random.choice(['Analista Jr', 'Analista Pl', 'Analista Sr', 'Coordenador', 'Gerente']),
            'age_range': np.random.choice(['18-25', '26-35', '36-45', '46-60+']),
            'tenure_months': np.random.randint(1, 120),
            'target': 0
        }
        
        # Questões Likert com padrão: ativos mais satisfeitos
        base_satisfaction = np.random.normal(3.5, 0.8)
        for q in range(1, 26):
            noise = np.random.normal(0, 0.3)
            score = np.clip(base_satisfaction + noise, 1, 5)
            row[f'q{q}'] = int(round(score))
        
        active_data.append(row)
    
    # Ex-colaboradores (desligamento)
    exit_data = []
    for i in range(n_exit):
        row = {
            'response_id': f'exit_{i}',
            'form_type': 'desligamento', 
            'employee_id': f'ex_emp_{i}',
            'sede': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Brasília', 'Recife']),
            'cargo': np.random.choice(['Analista Jr', 'Analista Pl', 'Analista Sr', 'Coordenador', 'Gerente']),
            'age_range': np.random.choice(['18-25', '26-35', '36-45', '46-60+']),
            'tenure_months': np.random.randint(3, 60),
            'tipo_desligamento': np.random.choice(['Voluntário', 'Involuntário', 'Acordo Mútuo']),
            'faltas_6m': np.random.randint(0, 15),
            'target': 1
        }
        
        # Questões Likert com padrão: ex-colaboradores mais insatisfeitos
        base_satisfaction = np.random.normal(2.2, 0.8)
        for q in range(1, 26):
            noise = np.random.normal(0, 0.4)
            score = np.clip(base_satisfaction + noise, 1, 5)
            row[f'q{q}'] = int(round(score))
        
        exit_data.append(row)
    
    # Combinar dados
    df = pd.DataFrame(active_data + exit_data)
    df['data_quality_flag'] = 'OK'
    df['created_at'] = datetime.now()
    
    return df

def main():
    os.makedirs('data', exist_ok=True)
    df = generate_sample_data()
    df.to_csv('data/sample_data.csv', index=False)
    print(f"Generated {len(df)} sample records")
    print(f"Active: {len(df[df.target==0])}, Exit: {len(df[df.target==1])}")
    print("Saved to data/sample_data.csv")

if __name__ == '__main__':
    main()
