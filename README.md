# People Analytics - Sistema de Análise de Turnover

## 🎯 Visão Geral

Sistema completo de análise de turnover que utiliza Random Forest para predizer saídas de colaboradores, fornecendo insights acionáveis para retenção de talentos.

### Características Principais

✅ **Coleta de Dados**: Google Forms (Pesquisa de Clima + Entrevista de Desligamento)  
✅ **Processamento**: Pipeline ETL automático com feature engineering  
✅ **Modelagem**: Random Forest com validação cruzada e otimização de hiperparâmetros  
✅ **Explicabilidade**: Análise SHAP para interpretação de resultados  
✅ **API**: FastAPI para predições em tempo real  
✅ **Dashboard**: Interface Angular + visualizações BI  
✅ **Recomendações**: Ações personalizadas para retenção  

---

## 📋 Índice

- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pipeline de Dados](#pipeline-de-dados)
- [API Endpoints](#api-endpoints)
- [Dashboard](#dashboard)
- [Contribuição](#contribuição)

---

## 🏗️ Arquitetura

```
Google Forms (Coleta)
         ↓
Python ETL (Processamento)
         ↓
PostgreSQL (Armazenamento)
         ↓
Random Forest (Modelagem)
         ↓
FastAPI (Predições)
         ↓
Angular Dashboard (Interface)
```

### Stack Tecnológico

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| **Coleta** | Google Forms + Google Sheets | Acessível, integração fácil |
| **ETL** | Python (Pandas, NumPy) | Processamento eficiente |
| **Storage** | PostgreSQL | Dados estruturados, ACID |
| **Modelagem** | Scikit-learn, SHAP | Random Forest + explicabilidade |
| **API** | FastAPI | Performance, documentação automática |
| **Frontend** | Angular 16+ | SPA moderna, componentes |
| **Deploy** | Docker | Containerização |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Docker (opcional)

### Setup Rápido

```bash
# 1. Clone o repositório
git clone https://github.com/lucasprac/people-analytics-turnover.git
cd people-analytics-turnover

# 2. Backend (API)
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# 3. Frontend (Angular)
cd ../frontend
npm install
ng serve

# 4. Database
psql -U postgres -c "CREATE DATABASE people_analytics;"
python scripts/setup_database.py
```

### Deploy com Docker

```bash
docker-compose up -d
```

---

## 💡 Uso

### 1. Coleta de Dados

1. Configure os Google Forms usando os templates em `/forms/`
2. Execute o ETL para processar respostas:

```bash
python scripts/extract_google_forms.py
python scripts/transform_features.py
```

### 2. Treinamento do Modelo

```bash
python scripts/train_model.py
python scripts/explain_shap.py
```

### 3. Predições

```bash
# API
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"satisfacao_media": 3.2, "gestor_media": 2.1, ...}'

# Dashboard
# Acesse: http://localhost:4200
```

---

## 📁 Estrutura do Projeto

```
people-analytics-turnover/
├── backend/                 # API FastAPI
│   ├── main.py             # Servidor principal
│   ├── models/             # Modelos Pydantic
│   ├── services/           # Lógica de negócio
│   └── requirements.txt    # Dependências Python
├── frontend/               # Dashboard Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/ # Componentes UI
│   │   │   └── services/   # Serviços HTTP
│   │   └── assets/         # Recursos estáticos
│   └── package.json        # Dependências Node.js
├── scripts/                # Scripts ETL e ML
│   ├── extract_google_forms.py
│   ├── transform_features.py
│   ├── train_model.py
│   └── explain_shap.py
├── models/                 # Modelos treinados
├── data/                   # Dados processados
├── forms/                  # Templates Google Forms
├── sql/                    # Scripts SQL
├── docs/                   # Documentação
└── docker-compose.yml      # Deploy
```

---

## 🔄 Pipeline de Dados

### Fluxo ETL

1. **Extract**: Download de respostas do Google Sheets
2. **Transform**: 
   - Validação de qualidade
   - Feature engineering (médias por tema, red flags)
   - Normalização demográfica
3. **Load**: Inserção no PostgreSQL

### Features Principais

- **Temas de Satisfação**: 5 dimensões (Trabalho, Recompensa, Gestor, WLB, Ambiente)
- **Scores Derivados**: Red flags, volatilidade, interações
- **Demográficos**: Sede, cargo, idade, tempo de empresa

---

## 🔌 API Endpoints

### Predição

```http
POST /predict
Content-Type: application/json

{
  "satisfacao_media": 3.2,
  "gestor_media": 2.1,
  "recompensa_media": 2.8,
  "wlb_media": 3.5,
  "red_flag_count": 5,
  ...
}
```

**Resposta:**

```json
{
  "risk_score": 0.73,
  "risk_level": "ALTO",
  "top_drivers": [
    {"feature": "gestor_media", "shap_value": 0.15},
    {"feature": "recompensa_media", "shap_value": 0.12}
  ],
  "suggested_actions": [
    "Avaliar relacionamento com gestor",
    "Revisar salário/benefícios"
  ]
}
```

### Outros Endpoints

- `GET /health` - Status da API
- `GET /metrics` - Métricas do modelo
- `POST /retrain` - Retreinar modelo

---

## 📊 Dashboard

### Visualizações

1. **Visão Executiva**: KPIs, distribuição de risco
2. **Drill-down**: Score individual, comparações
3. **Drivers**: Análise SHAP, correlações
4. **ROI**: Histórico de intervenções, taxa de sucesso

### Componentes Angular

- `RiskDashboardComponent`: Lista de colaboradores
- `RiskCardComponent`: Card individual
- `ShapVisualizationComponent`: Explicabilidade
- `InterventionTrackingComponent`: Acompanhamento de ações

---

## 🎯 Métricas de Sucesso

| Métrica | Target |
|---------|---------|
| **Recall** | ≥65% |
| **Precision** | ≥50% |
| **AUC-ROC** | ≥0.80 |
| **ROI Intervenções** | ≥2:1 |

---

## 🔒 Segurança e Privacidade

- ✅ Dados anonimizados (sem nomes reais)
- ✅ Criptografia HTTPS/SSL
- ✅ Controle de acesso (RH/gestores)
- ✅ Conformidade LGPD/GDPR
- ✅ Audit trail completo

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Suporte

Para dúvidas ou suporte, abra uma [issue](https://github.com/lucasprac/people-analytics-turnover/issues) ou entre em contato:

- **Email**: [seu-email@empresa.com]
- **Slack**: #people-analytics

---

**Desenvolvido com ❤️ para revolucionar People Analytics**