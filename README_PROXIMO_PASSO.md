# Ada — Principal Advisor | Próximo Passo do Projeto

Este pacote contém a atualização da base de conhecimento e da estrutura de dados para deixar o projeto aderente ao lab da DIO e, ao mesmo tempo, mais avançado.

## Como aplicar no repositório

Copie as pastas e arquivos deste pacote para a raiz do seu repositório:

```bash
docs/
data/
src/
tests/
scripts/
requirements.txt
```

## Como validar

Na raiz do projeto:

```bash
python scripts/validate_data.py
```

Para rodar testes:

```bash
pip install -r requirements.txt
pytest -q
```

## Entregáveis principais

- `docs/01-documentacao-agente.md`
- `docs/02-base-conhecimento.md`
- `data/perfil_investidor.json`
- `data/produtos_financeiros.json`
- `data/transacoes.csv`
- `data/historico_atendimento.csv`
- `data/crm/*`
- `src/safety.py`
- `src/recommender.py`
- `src/data_loader.py`
- `tests/test_data_integrity.py`


## Etapa 4 — Aplicação Funcional em Streamlit

Arquivos adicionados:

- `app.py`
- `src/ada_engine.py`
- `src/card_engine.py`
- `src/intent_router.py`
- `src/analytics.py`
- `scripts/validate_app.py`
- `tests/test_app_core.py`
- `docs/04-aplicacao-streamlit.md`

### Rodar aplicação

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Validar aplicação

```bash
python scripts/validate_app.py
pytest -q
```


## Complemento — Compatibilidade Multi-LLM

A aplicação agora roda em dois modos:

1. **Mock/local:** não usa API externa e funciona imediatamente.
2. **LLM real:** usa OpenAI/ChatGPT API, Gemini, Claude, Qwen ou endpoint OpenAI-compatible.

### Instalação básica

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Instalação com provedores LLM

```bash
pip install -r requirements.txt
pip install -r requirements-llm.txt
```

Configure as variáveis de ambiente usando `.env.example` como referência.

### Validar compatibilidade Multi-LLM

```bash
python scripts/validate_llm_compatibility.py
pytest -q
```

### Observação

O Streamlit não roda "dentro" do ChatGPT, Gemini ou Claude como interface nativa. O que o projeto faz é usar esses modelos como camada de raciocínio por API. Para uso em Custom GPT, Gemini Gems ou Claude Projects, reaproveite os prompts e a base de conhecimento, ou exponha a aplicação como API externa.


## Etapa 5 — Métricas, Avaliação e Testes de Qualidade

Arquivos adicionados:

- `data/evaluation/perguntas_teste.csv`
- `data/evaluation/casos_criticos.csv`
- `data/evaluation/cenarios_recomendacao_cartoes.csv`
- `data/evaluation/rubrica_avaliacao.json`
- `src/evaluator.py`
- `scripts/run_evaluation.py`
- `scripts/validate_evaluation.py`
- `tests/test_evaluation.py`
- `docs/06-metricas-avaliacao.md`

### Validar avaliação

```bash
python scripts/validate_evaluation.py
```

### Rodar avaliação

```bash
python scripts/run_evaluation.py
```

### Rodar todos os testes

```bash
pytest -q
```


## Etapa 5.1 — Polimento Nota 10

Melhorias aplicadas:

- `data/evaluation/solicitacoes_nota_1_10.csv` expandido para 20 solicitações;
- régua mínima elevada para nota 10;
- `data/evaluation/feedback_humano_exemplo_simulado_1_10.csv`;
- `docs/04-metricas.md` com matriz executiva;
- `app.py` com nova aba `Avaliação & Métricas`;
- novos testes para garantir nota 10, métricas e dashboard.

### Rodar avaliação nota 10

```bash
python scripts/run_evaluation.py
pytest -q
```


## Etapa 6 — README Final e Pitch

Arquivos adicionados/atualizados:

- `README.md`
- `docs/05-pitch.md`
- `scripts/validate_readme_pitch.py`
- `tests/test_readme_pitch.py`

### Validar README e Pitch

```bash
python scripts/validate_readme_pitch.py
pytest -q
```


## Etapa 7 — Revisão Final e Pacote Pronto para GitHub

Arquivos adicionados:

- `CHECKLIST_ENTREGA.md`
- `docs/07-revisao-final-github.md`
- `scripts/validate_final_package.py`
- `tests/test_final_package.py`

### Validar pacote final

```bash
python scripts/validate_final_package.py
pytest -q
```
