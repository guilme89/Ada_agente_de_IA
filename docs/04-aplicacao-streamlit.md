# Aplicação Funcional — Ada — Principal Advisor

## 1. Objetivo

Esta etapa transforma a Ada — Principal Advisor em uma aplicação funcional usando Streamlit.

A aplicação foi criada para demonstrar, de forma visual e interativa, como um agente consultivo pode combinar:

- base de conhecimento;
- CRM mockado;
- recomendação de cartão por aderência;
- segurança e guardrails;
- Next Best Action;
- visão 360º do cliente;
- diagnóstico consultivo;
- prompts especializados.

---

## 2. Arquivo principal

A aplicação roda a partir do arquivo:

```bash
streamlit run app.py
```

---

## 3. Módulos criados

| Arquivo | Função |
|---|---|
| `app.py` | Interface principal em Streamlit. |
| `src/ada_engine.py` | Motor de resposta consultiva da Ada. |
| `src/card_engine.py` | Motor de recomendação de cartão por aderência. |
| `src/intent_router.py` | Detector simples de intenção do usuário. |
| `src/analytics.py` | Funções para métricas, visão financeira e resumo CRM. |
| `src/prompt_loader.py` | Carregamento dos prompts. |
| `src/safety.py` | Bloqueio de dados sensíveis e respostas seguras. |

---

## 4. Abas da aplicação

### 4.1 Chat Ada

Permite conversar com a Ada usando uma persona mockada selecionada.

A Ada detecta intenção, aplica guardrails e responde de forma consultiva.

### 4.2 Cliente 360

Mostra uma visão completa do cliente mockado:

- segmento;
- temperatura do lead;
- score potencial;
- cartão recomendado;
- patrimônio investível mock;
- share wallet;
- gasto em cartão;
- resumo consultivo;
- histórico de 12 meses.

### 4.3 Simulador

Permite simular uma recomendação de cartão com base em:

- segmento;
- viagens;
- gasto mensal;
- patrimônio mockado;
- interesse em salas VIP;
- interesse em pontos;
- prioridade do cliente.

### 4.4 CRM Dashboard

Mostra indicadores agregados da base:

- total de personas;
- clientes Principal;
- clientes Prime com potencial;
- patrimônio investível mock;
- aporte previsto;
- distribuição por temperatura;
- segmentação psicológica financeira.

### 4.5 Next Best Action

Exibe a próxima melhor ação mockada para o cliente selecionado.

### 4.6 Segurança

Laboratório para testar bloqueio de dados sensíveis e respostas seguras.

### 4.7 Prompts

Central para visualizar os prompts carregados e o master prompt consolidado.

---

## 5. Guardrails implementados

A aplicação bloqueia ou recusa:

- CPF;
- número de cartão;
- telefone;
- e-mail;
- senha;
- CVV;
- pedido de limite aprovado;
- contratação real;
- consulta de dados bancários.

---

## 6. Limitações

A aplicação é educacional e não oficial.

Ela não:

- consulta sistemas reais;
- usa dados reais;
- aprova cartão;
- informa limite;
- realiza contratação;
- substitui gerente;
- representa atendimento oficial do Bradesco.

---

## 7. Como testar

Instalar dependências:

```bash
pip install -r requirements.txt
```

Validar dados:

```bash
python scripts/validate_data.py
```

Validar prompts:

```bash
python scripts/validate_prompt_suite.py
```

Validar app:

```bash
python scripts/validate_app.py
```

Rodar testes:

```bash
pytest -q
```

Rodar aplicação:

```bash
streamlit run app.py
```

---

## 8. Diferencial da etapa

Esta etapa transforma o projeto em uma experiência demonstrável.

O avaliador consegue ver:

- dados carregando;
- CRM funcionando;
- recomendação acontecendo;
- segurança bloqueando dados sensíveis;
- Next Best Action sendo apresentada;
- prompts estruturados;
- app navegável e profissional.
