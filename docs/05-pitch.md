# Pitch (3 minutos) — Ada — Principal Advisor

> Roteiro final para gravação do pitch do projeto.  
> Duração alvo: **até 3 minutos**.

---

## Roteiro Sugerido

### 1. O Problema (30 seg)

Clientes de alta renda têm muitas opções de cartões, benefícios, pontos, salas VIP, anuidade, serviços digitais e relacionamento financeiro. Mas, na prática, comparar tudo isso de forma clara não é simples.

Além disso, quando falamos de produtos financeiros, existe um risco importante: uma recomendação mal feita pode gerar venda inadequada, promessa indevida, exposição de dados sensíveis ou até facilitar golpes.

A dor que este projeto resolve é: **como orientar o cliente de forma consultiva, personalizada e segura, sem transformar a IA em um canal de promessa, aprovação ou coleta de dados sensíveis?**

---

### 2. A Solução (1 min)

Para resolver esse problema, eu desenvolvi a **Ada — Principal Advisor**, um agente inteligente educacional e não oficial, criado para simular uma jornada premium de atendimento consultivo no contexto Bradesco Principal.

A Ada entende o perfil informado, consulta uma base de conhecimento, usa uma base CRM sintética com 100 personas, analisa histórico simulado de relacionamento, eventos de vida, comportamento de cartão, Open Finance mockado e Next Best Action.

Com isso, ela recomenda o cartão com maior aderência ao perfil informado, como Visa Aeternum, The Platinum Card® ou Bradesco Principal, sempre de forma educativa e consultiva.

O ponto mais importante é que a Ada não promete aprovação, não informa limite, não realiza contratação e não solicita CPF, senha, CVV, número de cartão, fatura ou extrato.

O projeto também foi preparado para rodar com diferentes modelos de linguagem, como OpenAI/ChatGPT, Gemini, Claude, Qwen ou modo mock local, usando uma arquitetura Multi-LLM com fallback seguro.

---

### 3. Demonstração (1 min)

Na demonstração, eu mostro a aplicação funcionando em Streamlit.

Primeiro, abro o **Chat Ada** e faço uma pergunta como: “Viajo bastante e valorizo salas VIP. Qual cartão tem maior aderência?” A Ada identifica a intenção, recomenda o Visa Aeternum por aderência e finaliza com orientação para canais oficiais.

Depois, mostro a aba **Cliente 360**, onde a aplicação apresenta uma persona mockada com segmento, temperatura do lead, score potencial, patrimônio investível fictício, gasto no cartão, resumo consultivo e histórico de 12 meses.

Na aba **Next Best Action**, mostro a próxima melhor ação sugerida para aquele perfil, como retenção, conversa com gerente, Open Finance mockado ou revisão de planejamento.

Em seguida, abro o laboratório de **Segurança** e testo uma mensagem com CPF, senha ou CVV. A Ada bloqueia a solicitação e responde com segurança.

Por fim, mostro a aba **Avaliação & Métricas**, onde o projeto apresenta 100% de aprovação nos testes, nota média 10, nota mínima 10, 100% de segurança e unsafe output rate de 0%.

---

### 4. Diferencial e Impacto (30 seg)

O diferencial deste projeto é que ele não é apenas um chatbot. Ele combina IA generativa, CRM, dados mockados, recomendação consultiva, segurança, guardrails, Multi-LLM, métricas e avaliação automatizada.

O impacto está em mostrar como uma IA financeira pode ser útil sem abrir mão de responsabilidade. A Ada ajuda a educar, orientar, comparar opções e conduzir a próxima melhor ação, mas respeitando limites de privacidade, segurança e governança.

Em uma aplicação real, esse tipo de solução poderia melhorar a experiência do cliente, apoiar gerentes, reduzir dúvidas repetitivas, aumentar segurança digital e tornar a recomendação de produtos mais clara, responsável e aderente ao perfil.

---

## Versão Corrida para Gravação

Olá, meu nome é Guilherme Ferreira Fontoura e este é o projeto **Ada — Principal Advisor**.

O problema que eu quis resolver é muito comum no mercado financeiro: clientes de alta renda têm muitas opções de cartões, benefícios, pontos, salas VIP e serviços premium, mas nem sempre conseguem entender qual opção faz mais sentido para o seu perfil.

Além disso, existe um risco importante. Uma IA financeira não pode prometer aprovação, informar limite, coletar dados sensíveis ou inventar regras de banco. Ela precisa ser consultiva, mas também segura.

Por isso eu desenvolvi a Ada, um agente inteligente educacional e não oficial, criado para simular uma jornada premium de atendimento consultivo no contexto Bradesco Principal.

A Ada analisa o perfil informado, usa uma base CRM sintética com 100 personas, histórico de relacionamento simulado, eventos de vida, comportamento de cartão, Open Finance mockado e Next Best Action. Com isso, ela recomenda o cartão com maior aderência ao perfil, como Visa Aeternum, The Platinum Card® ou Bradesco Principal.

Agora vou mostrar a aplicação funcionando.

Aqui no Chat Ada, eu pergunto: “Viajo bastante e valorizo salas VIP. Qual cartão tem maior aderência?” A Ada entende o contexto, recomenda o Visa Aeternum por aderência e reforça que aprovação, limite e contratação precisam ser confirmados nos canais oficiais.

Na aba Cliente 360, vemos uma persona mockada com segmento, temperatura do lead, patrimônio fictício, gasto no cartão, histórico de 12 meses e resumo consultivo.

Na aba Next Best Action, a aplicação mostra a próxima melhor ação para o cliente, como conversa com gerente, retenção consultiva, Open Finance mockado ou revisão de planejamento.

Também existe uma aba de Segurança. Se o usuário envia CPF, senha, número de cartão ou CVV, a Ada bloqueia a solicitação e orienta o uso dos canais oficiais.

Por fim, na aba Avaliação & Métricas, o projeto mostra a qualidade técnica da solução: 100% de aprovação nos testes, 100% de segurança, 100% de casos críticos aprovados, nota média 10, nota mínima 10 e unsafe output rate de 0%.

O grande diferencial da Ada é unir IA generativa, dados, CRM, recomendação consultiva, guardrails, Multi-LLM e avaliação automatizada em uma única solução.

Esse projeto mostra como uma IA financeira pode gerar valor, orientar melhor o cliente e apoiar decisões, sem abrir mão de segurança, privacidade e responsabilidade.

---

## Demonstração — Ordem Recomendada da Gravação

1. Abrir a tela inicial do Streamlit.
2. Mostrar rapidamente o aviso de projeto educacional e não oficial.
3. Entrar no **Chat Ada**.
4. Fazer pergunta sobre viagem e sala VIP.
5. Mostrar recomendação por aderência.
6. Abrir **Cliente 360**.
7. Mostrar resumo, score, patrimônio mockado e histórico.
8. Abrir **Next Best Action**.
9. Mostrar ação recomendada.
10. Abrir **Segurança**.
11. Testar mensagem com dado sensível.
12. Abrir **Avaliação & Métricas**.
13. Mostrar nota 10, segurança 100% e testes aprovados.
14. Finalizar com diferencial e impacto.

---

## Checklist do Pitch

- [x] Duração máxima de 3 minutos
- [x] Problema claramente definido
- [x] Solução demonstrada na prática
- [x] Diferencial explicado
- [x] Segurança e privacidade mencionadas
- [x] Métricas e testes apresentados
- [x] Áudio e vídeo com boa qualidade
- [x] Demonstração objetiva, sem navegar demais
- [x] Aviso de projeto educacional e não oficial

---

## Link do Vídeo

> Cole aqui o link do seu pitch quando gravar.

[Link do vídeo]

---

## Observações Finais

Este pitch foi estruturado para valorizar o que o projeto tem de mais forte:

- aplicação funcional;
- uso de dados mockados;
- recomendação consultiva;
- Multi-LLM;
- segurança;
- métricas;
- avaliação automatizada;
- aderência ao desafio.
