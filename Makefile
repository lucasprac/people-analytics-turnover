# Makefile para automação de tarefas

.PHONY: help setup install run-backend run-frontend run-docker clean test

# Variáveis
PYTHON := python3
NODE := node
NPM := npm
DOCKER := docker
DOCKER_COMPOSE := docker-compose

help: ## Mostra esta mensagem de ajuda
	@echo "People Analytics - Turnover Prediction System"
	@echo "============================================="
	@echo ""
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Configura o ambiente inicial
	@echo "Configurando ambiente..."
	@chmod +x scripts/*.sh
	@./scripts/quick_start.sh

install: ## Instala dependências
	@echo "Instalando dependências do backend..."
	cd backend && pip3 install -r requirements.txt
	@echo "Instalando dependências do frontend..."
	cd frontend && npm install

run-backend: ## Executa o backend
	@echo "Iniciando backend em http://localhost:8000"
	cd backend && $(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-frontend: ## Executa o frontend 
	@echo "Iniciando frontend em http://localhost:4200"
	cd frontend && npm start

run-docker: ## Executa com Docker Compose
	@echo "Iniciando sistema com Docker..."
	$(DOCKER_COMPOSE) up -d
	@echo "Acesse: http://localhost:4200"

data-sample: ## Gera dados sintéticos para teste
	@echo "Gerando dados de exemplo..."
	$(PYTHON) scripts/generate_sample_data.py

data-extract: ## Extrai dados do Google Forms
	@echo "Extraindo dados dos formulários..."
	$(PYTHON) scripts/extract_google_forms.py

data-transform: ## Transforma dados em features
	@echo "Processando features..."
	$(PYTHON) scripts/transform_features.py

model-train: ## Treina o modelo Random Forest
	@echo "Treinando modelo..."
	$(PYTHON) scripts/train_model.py

model-explain: ## Gera análise SHAP
	@echo "Gerando explicabilidade SHAP..."
	$(PYTHON) scripts/explain_shap.py

pipeline-full: data-extract data-transform model-train model-explain ## Executa pipeline completo
	@echo "Pipeline completo executado!"

db-setup: ## Configura o banco de dados
	@echo "Configurando PostgreSQL..."
	$(PYTHON) scripts/setup_database.py

db-reset: ## Reset do banco de dados
	@echo "Resetando banco..."
	psql -U postgres -c "DROP DATABASE IF EXISTS people_analytics;"
	psql -U postgres -c "CREATE DATABASE people_analytics;"
	$(PYTHON) scripts/setup_database.py

test: ## Executa testes
	@echo "Executando testes..."
	# TODO: Adicionar testes automatizados

lint: ## Verifica qualidade do código
	@echo "Verificando qualidade do código Python..."
	flake8 backend/ scripts/ --max-line-length=100
	@echo "Verificando qualidade do código TypeScript..."
	cd frontend && npm run lint

clean: ## Limpa arquivos temporários
	@echo "Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf backend/.pytest_cache
	rm -rf frontend/node_modules/.cache

stop-docker: ## Para containers Docker
	@echo "Parando containers..."
	$(DOCKER_COMPOSE) down

logs: ## Mostra logs dos containers
	$(DOCKER_COMPOSE) logs -f

# Comandos de desenvolvimento
dev-backend: ## Desenvolvimento backend com auto-reload
	@echo "Modo desenvolvimento - Backend"
	cd backend && $(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Desenvolvimento frontend com auto-reload
	@echo "Modo desenvolvimento - Frontend"
	cd frontend && ng serve --host 0.0.0.0 --port 4200

# Status do sistema
status: ## Verifica status dos serviços
	@echo "Status dos serviços:"
	@echo "Backend (8000): $$(curl -s http://localhost:8000/health | grep -o '"status":"OK"' || echo "OFF")"
	@echo "Frontend (4200): $$(curl -s http://localhost:4200 > /dev/null && echo "ON" || echo "OFF")"
	@echo "Database: $$(pg_isready -h localhost -p 5432 > /dev/null && echo "ON" || echo "OFF")"
