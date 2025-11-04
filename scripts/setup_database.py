#!/usr/bin/env python3
"""
Script para configurar o banco de dados PostgreSQL
"""
import os
import psycopg2
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres123@localhost:5432/people_analytics')

def create_database():
    """Cria o banco se não existir"""
    try:
        engine = create_engine(DATABASE_URL.replace('/people_analytics', '/postgres'))
        with engine.connect() as conn:
            conn.execute(text("COMMIT"))
            conn.execute(text("CREATE DATABASE people_analytics"))
        print("Database created successfully!")
    except Exception as e:
        print(f"Database may already exist: {e}")

def setup_tables():
    """Cria as tabelas usando o SQL init"""
    engine = create_engine(DATABASE_URL)
    with open('sql/init.sql', 'r') as f:
        sql = f.read()
    
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print("Tables created successfully!")

if __name__ == '__main__':
    create_database()
    setup_tables()
