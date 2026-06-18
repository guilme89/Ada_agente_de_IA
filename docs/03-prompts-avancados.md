# Prompts Avançados, Guardrails e Regras de Decisão

## 1. Objetivo

Esta etapa amplia a camada de prompts da Ada — Principal Advisor para aproximar o projeto de uma solução avançada de Data-Driven Banking.

A Ada passa a contar com prompts especializados para:

- privacidade e LGPD;
- anti-alucinação;
- diagnóstico consultivo;
- vendas consultivas responsáveis;
- Next Best Action;
- handoff para canais oficiais;
- segurança digital e prevenção a golpes;
- resumo CRM;
- avaliação de respostas.

---

## 2. Arquivos Criados

| Arquivo | Função |
|---|---|
| `guardrails_privacidade_lgpd.md` | Define limites de dados, minimização, consentimento e privacidade por padrão. |
| `guardrails_anti_alucinacao.md` | Define como a Ada evita inventar taxas, regras, limites ou condições. |
| `roteiro_diagnostico_consultivo.md` | Conduz a jornada consultiva antes da recomendação. |
| `nba_playbook.md` | Define lógica de Next Best Action mockada. |
| `politica_handoff.md` | Define quando encaminhar para gerente, app, Internet Banking ou canais oficiais. |
| `vendas_consultivas_responsaveis.md` | Permite abordagem comercial sem pressão, promessa ou risco. |
| `seguranca_golpes.md` | Regras de resposta para links suspeitos, falsa central, motoboy e fraude. |
| `avaliador_respostas.md` | Checklist para medir qualidade e segurança das respostas. |
| `resumo_cliente_crm.md` | Prompt para gerar resumo executivo de cliente mockado. |

---

## 3. Ganho para o Projeto

Com essa camada, a Ada deixa de ser apenas um agente de perguntas e respostas e passa a simular uma operação consultiva mais robusta:

1. Diagnóstico antes da recomendação.
2. Recomendação por aderência.
3. Venda consultiva responsável.
4. Segurança e privacidade por padrão.
5. Handoff correto para canal oficial.
6. Uso transparente de dados mockados.
7. Redução de alucinação.
8. Capacidade de avaliação de respostas.
9. Apoio a CRM e Next Best Action.

---

## 4. Critérios de Integridade

A etapa é considerada íntegra quando:

- todos os prompts carregam corretamente;
- há pelo menos 13 arquivos de prompt;
- os conceitos obrigatórios aparecem na suíte;
- não há promessas proibidas;
- os testes automatizados passam;
- os scripts de validação retornam sucesso.

---

## 5. Relação com a Aplicação

Na etapa 4, a aplicação em Streamlit poderá carregar os prompts de duas formas:

1. Prompt principal para identidade e comportamento.
2. Prompts especializados conforme intenção detectada.

Exemplos:

- Pergunta com dado sensível: usar guardrail de LGPD.
- Pergunta sobre cartão: usar regras de recomendação.
- Pergunta sobre golpe: usar segurança digital.
- Pedido de resumo CRM: usar resumo de cliente.
- Resposta gerada: avaliar com checklist de qualidade.
