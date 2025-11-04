# Contributing Guidelines

## Como Contribuir

Obrigado por considerar contribuir com o People Analytics - Sistema de Análise de Turnover!

## Processo de Desenvolvimento

### 1. Setup do Ambiente

```bash
# Clone o repositório
git clone https://github.com/lucasprac/people-analytics-turnover.git
cd people-analytics-turnover

# Configure o ambiente
make setup
```

### 2. Branches

- `main`: Produção
- `development`: Desenvolvimento
- `feature/nome-da-feature`: Novas funcionalidades
- `fix/nome-do-bug`: Correções

### 3. Padrões de Código

#### Python (Backend/Scripts)
- PEP 8 compliance
- Type hints quando possível
- Docstrings para funções
- Máximo 100 caracteres por linha

#### TypeScript (Frontend)
- Angular style guide
- Prettier para formatação
- ESLint para qualidade
- Nomenclatura camelCase

#### SQL
- Nomes de tabelas em snake_case
- UPPERCASE para palavras-chave
- Indentação consistente

### 4. Commits

Use conventional commits:

```
feat: adiciona novo endpoint de métricas
fix: corrige cálculo de risk_score
docs: atualiza README com instruções
refactor: reorganiza estrutura de pastas
test: adiciona testes unitários para ETL
```

### 5. Pull Requests

1. Crie uma branch a partir de `development`
2. Faça suas alterações
3. Execute os testes: `make test`
4. Verifique lint: `make lint`
5. Abra um PR para `development`

#### Template de PR

```markdown
## Descrição

Breve descrição das mudanças

## Tipo de Mudança

- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Checklist

- [ ] Código testado
- [ ] Lint passou
- [ ] Documentação atualizada
- [ ] CHANGELOG atualizado
```

### 6. Reporting Issues

Ao reportar bugs, inclua:
- Versão do sistema
- Passos para reproduzir
- Comportamento esperado
- Logs relevantes

## Estrutura do Projeto

```
people-analytics-turnover/
├── backend/           # API FastAPI
├── frontend/          # App Angular
├── scripts/           # Scripts ETL/ML
├── sql/               # Scripts SQL
├── forms/             # Templates Forms
├── docs/              # Documentação
├── models/            # Modelos treinados
└── data/              # Dados processados
```

## Guidelines de Segurança

- Não commitar credenciais
- Usar variáveis de ambiente
- Validar inputs da API
- Sanitizar dados sensíveis
- Implementar auditoria

## Performance

- Otimizar queries SQL
- Implementar cache quando necessário
- Monitorar métricas de modelo
- Considerar escalabilidade

## Testes

- Testes unitários para lógica de negócio
- Testes de integração para API
- Testes de qualidade de dados
- Testes de performance do modelo

## Documentação

- README atualizado
- Docstrings em funções
- API docs (FastAPI/Swagger)
- Changelog mantido

---

**Obrigado por contribuir! 🚀**
