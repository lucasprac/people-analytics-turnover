#!/bin/bash

# Setup do banco de dados PostgreSQL
echo "Setting up PostgreSQL database..."

# Cria o banco se não existir
psql -U postgres -c "CREATE DATABASE people_analytics;" 2>/dev/null || echo "Database already exists"

# Executa os scripts SQL
psql -U postgres -d people_analytics -f sql/init.sql

echo "Database setup completed!"
