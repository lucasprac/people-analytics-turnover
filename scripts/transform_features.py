"""
Transforma respostas em features para modelagem
"""
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres123@localhost:5432/people_analytics')


def theme_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    qmap = {
        'satisfacao': [f'q{i}' for i in range(1, 6) if f'q{i}' in df.columns],
        'recompensa': [f'q{i}' for i in range(6, 11) if f'q{i}' in df.columns],
        'gestor': [f'q{i}' for i in range(11, 16) if f'q{i}' in df.columns],
        'wlb': [f'q{i}' for i in range(16, 21) if f'q{i}' in df.columns],
        'ambiente': [f'q{i}' for i in range(21, 26) if f'q{i}' in df.columns],
    }
    for theme, qs in qmap.items():
        if qs:
            df[f'{theme}_media'] = df[qs].mean(axis=1)
            df[f'{theme}_std'] = df[qs].std(axis=1)
        else:
            df[f'{theme}_media'] = np.nan
            df[f'{theme}_std'] = np.nan
    return df


def derived_features(df: pd.DataFrame) -> pd.DataFrame:
    qs = [f'q{i}' for i in range(1, 26) if f'q{i}' in df.columns]
    if qs:
        df['satisfacao_geral_media'] = df[qs].mean(axis=1)
        df['satisfacao_geral_std'] = df[qs].std(axis=1)
        df['red_flag_count'] = (df[qs] <= 2).sum(axis=1)
        df['yellow_flag_count'] = (df[qs] == 3).sum(axis=1)
    else:
        df['satisfacao_geral_media'] = np.nan
        df['satisfacao_geral_std'] = np.nan
        df['red_flag_count'] = 0
        df['yellow_flag_count'] = 0
    df['interaction_gestor_recompensa'] = df.get('gestor_media', 0) * df.get('recompensa_media', 0)
    df['interaction_wlb_satisfacao'] = df.get('wlb_media', 0) * df.get('satisfacao_media', 0)
    return df


def normalize_demo(df: pd.DataFrame) -> pd.DataFrame:
    if 'sede' in df.columns:
        df = pd.get_dummies(df, columns=['sede'], prefix='sede', drop_first=True)
    if 'cargo' in df.columns:
        df['cargo_encoded'] = df['cargo'].astype('category').cat.codes
    if 'age_range' in df.columns:
        order = ['18-25', '26-35', '36-45', '46-60+']
        df['age_encoded'] = df['age_range'].map({v: i for i, v in enumerate(order)}).fillna(0).astype(int)
    if 'tenure_months' in df.columns:
        t = df['tenure_months']
        df['tenure_normalized'] = (t - t.min()) / (t.max() - t.min() + 1e-6)
    return df


def select_features(df: pd.DataFrame) -> pd.DataFrame:
    base = [
        'satisfacao_media','satisfacao_std','recompensa_media','recompensa_std','gestor_media','gestor_std',
        'wlb_media','wlb_std','ambiente_media','ambiente_std','satisfacao_geral_media','satisfacao_geral_std',
        'red_flag_count','yellow_flag_count','interaction_gestor_recompensa','interaction_wlb_satisfacao',
        'cargo_encoded','age_encoded','tenure_normalized','target'
    ]
    sede_cols = [c for c in df.columns if c.startswith('sede_')]
    cols = [c for c in base if c in df.columns] + sede_cols
    return df[cols]


def save(df: pd.DataFrame):
    engine = create_engine(DATABASE_URL)
    df.to_sql('processed_features', engine, if_exists='append', index=False)
    os.makedirs('data', exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    df.to_csv(f'data/processed_features_{ts}.csv', index=False)


def main():
    engine = create_engine(DATABASE_URL)
    raw = pd.read_sql('SELECT * FROM raw_responses', engine)
    df = theme_aggregates(raw)
    df = derived_features(df)
    df = normalize_demo(df)
    proc = select_features(df)
    save(proc)
    print(f"Processed {len(proc)} rows with {len(proc.columns)} features")


if __name__ == '__main__':
    main()
