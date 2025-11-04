"""
Extrai respostas dos Google Sheets e carrega na tabela raw_responses
"""
import pandas as pd
import gspread
from sqlalchemy import create_engine
from datetime import datetime
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres123@localhost:5432/people_analytics')


def extract_sheet(sheet_name: str):
    gc = gspread.service_account(filename='service_account.json')
    ws = gc.open(sheet_name).sheet1
    data = ws.get_all_records()
    return pd.DataFrame(data)


def validate_and_flag(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = [f'q{i}' for i in range(1, 26) if f'q{i}' in df.columns]
    df['data_quality_flag'] = 'OK'
    if required_cols:
        duplicated = df[df.duplicated(subset=required_cols, keep=False)]
        df.loc[duplicated.index, 'data_quality_flag'] = 'suspicious'
        all_same = (df[required_cols].nunique(axis=1) == 1)
        df.loc[all_same, 'data_quality_flag'] = 'suspicious'
        volatility = df[required_cols].std(axis=1)
        df.loc[volatility > 2, 'data_quality_flag'] = 'suspicious'
    return df


def anonymize(df: pd.DataFrame) -> pd.DataFrame:
    for col in ['Nome', 'Email', 'name', 'email']:
        if col in df.columns:
            df = df.drop(columns=[col])
    df['employee_id'] = pd.util.hash_pandas_object(df.index, index=True).values.astype('uint64').astype(str).str[:10]
    return df


def save_to_db(df: pd.DataFrame):
    engine = create_engine(DATABASE_URL)
    df.to_sql('raw_responses', engine, if_exists='append', index=False)


def main():
    clima = extract_sheet('Pesquisa de Clima 2025')
    deslig = extract_sheet('Entrevista de Desligamento 2025')
    clima['form_type'] = 'clima'; clima['target'] = 0
    deslig['form_type'] = 'desligamento'; deslig['target'] = 1

    df = pd.concat([clima, deslig], ignore_index=True)
    df = validate_and_flag(df)
    df = anonymize(df)

    os.makedirs('data', exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    df.to_csv(f'data/raw_responses_{ts}.csv', index=False)
    save_to_db(df)
    print(f"Saved {len(df)} responses to DB and CSV")


if __name__ == '__main__':
    main()
