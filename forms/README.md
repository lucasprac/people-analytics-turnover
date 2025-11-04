# Templates Google Forms

Este diretório contém os templates dos formulários Google Forms.

## Formulário 1: Pesquisa de Clima (Colaboradores Ativos)

**Objetivo**: Coletar dados de colaboradores ativos (Classe 0)
**Frequência**: Semestral/Anual
**Respondentes**: Todos colaboradores ativos
**Tempo**: ~10 minutos

### Estrutura:

1. **Dados Demográficos**
   - Sede (dropdown)
   - Cargo (dropdown) 
   - Faixa de Idade (18-25, 26-35, 36-45, 46-60+)
   - Tempo de Empresa (meses)

2. **25 Questões Likert (1-5)**
   - Satisfação no Trabalho (Q1-Q5)
   - Recompensa e Crescimento (Q6-Q10)
   - Relacionamento com Gestor (Q11-Q15)
   - Equilíbrio Vida-Trabalho (Q16-Q20)
   - Satisfação com Ambiente (Q21-Q25)

3. **3 Questões Abertas** (texto livre)
4. **1 Consentimento LGPD** (checkbox)

---

## Formulário 2: Entrevista de Desligamento (Colaboradores que Saíram)

**Objetivo**: Coletar dados de ex-colaboradores (Classe 1)
**Frequência**: A cada desligamento
**Respondentes**: Todos que saem
**Tempo**: ~15 minutos

### Estrutura:

1. **Dados Demográficos**
   - Data admissão
   - Data desligamento
   - Tempo de casa
   - Sede, Cargo, Idade
   - Faltas últimos 6 meses
   - Tipo desligamento

2. **Mesmas 25 Questões Likert** (comparabilidade)
3. **3 Questões Abertas**
4. **Consentimento LGPD**

---

## Configuração

- Respostas armazenadas automaticamente no Google Sheets
- Exportação automática para CSV
- Anonimização de dados sensíveis
- Validação de campos obrigatórios
- Ranges Likert 1-5
