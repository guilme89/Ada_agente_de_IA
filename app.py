from __future__ import annotations

import sys
import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.append(str(SRC))

from data_loader import load_core_data, load_crm_data
from prompt_loader import load_all_prompts, build_master_prompt
from llm_client import SUPPORTED_PROVIDERS, DEFAULT_MODELS, get_provider_status
from ada_engine import generate_response, summarize_profile, money, pct
from card_engine import recommend_card_from_inputs, recommend_card_from_profile
from analytics import summarize_dataset, calculate_financial_snapshot, get_client_history, get_client_nba
from safety import validate_user_message


st.set_page_config(
    page_title="Ada — Principal Advisor",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def cached_core_data():
    return load_core_data()


@st.cache_data(show_spinner=False)
def cached_crm_data():
    crm = load_crm_data()
    return {
        "clientes": pd.DataFrame(crm["clientes"]),
        "historico_12m": pd.DataFrame(crm["historico_12m"]),
        "next_best_action": pd.DataFrame(crm["next_best_action"]),
        "base_consolidada": crm["base_consolidada"],
    }


@st.cache_data(show_spinner=False)
def cached_prompts():
    return load_all_prompts()


def as_number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0)


def select_profile(clientes: pd.DataFrame) -> dict:
    clientes = clientes.copy()
    clientes["label"] = (
        clientes["persona_id"].astype(str)
        + " | "
        + clientes["segmento_atual"].astype(str)
        + " | "
        + clientes.get("nome_ficticio", pd.Series(["Cliente mock"] * len(clientes))).astype(str)
    )
    label = st.sidebar.selectbox("Persona mockada para simulação", clientes["label"].tolist())
    persona_id = label.split(" | ")[0]
    return clientes[clientes["persona_id"] == persona_id].iloc[0].to_dict()


def render_header():
    st.title("💎 Ada — Principal Advisor")
    st.caption(
        "Protótipo educacional avançado de IA consultiva para cartões, CRM, planejamento financeiro, "
        "segurança digital e Next Best Action no contexto Bradesco Principal."
    )

    st.info(
        "Projeto educacional e não oficial. A Ada não representa atendimento real do Bradesco, "
        "não consulta dados bancários, não aprova crédito e não realiza contratação."
    )


def render_sidebar(clientes: pd.DataFrame):
    st.sidebar.title("Ada Principal")
    st.sidebar.caption("Data-Driven Banking | CRM Mock | Guardrails")
    profile = select_profile(clientes)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Perfil selecionado")
    st.sidebar.write(f"**Persona:** {profile.get('persona_id')}")
    st.sidebar.write(f"**Segmento:** {profile.get('segmento_atual')}")
    st.sidebar.write(f"**Temperatura:** {profile.get('temperatura_lead')}")
    st.sidebar.write(f"**Psicologia:** {profile.get('segmentacao_psicologica_mock', 'não informado')}")

    st.sidebar.markdown("---")
    st.sidebar.warning(
        "Não insira CPF, senha, número de cartão, CVV, fatura, extrato ou dados reais."
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("LLM Provider")
    use_llm = st.sidebar.toggle("Usar LLM real", value=False, help="Desligado usa motor determinístico local. Ligado chama o provedor selecionado.")
    provider = st.sidebar.selectbox("Provedor", list(SUPPORTED_PROVIDERS.keys()), index=0)
    default_model = DEFAULT_MODELS.get(provider, "model-name")
    model = st.sidebar.text_input("Modelo", value=default_model)

    statuses = get_provider_status()
    status = statuses.get(provider, {})
    if provider == "mock":
        st.sidebar.success("Modo mock/local ativo. Não usa API externa.")
    elif status.get("ready"):
        st.sidebar.success("Chave/endpoint configurado no ambiente.")
    else:
        st.sidebar.info("Configure variáveis de ambiente para ativar este provedor.")

    llm_settings = {
        "use_llm": use_llm,
        "provider": provider,
        "model": model,
        "status": status,
    }

    return profile, llm_settings


def tab_chat(profile: dict, nba_df: pd.DataFrame, products: list[dict], llm_settings: dict):
    st.subheader("💬 Chat consultivo da Ada")
    st.write("Converse com a Ada usando a persona mockada selecionada na barra lateral.")

    examples = [
        "Qual cartão tem maior aderência para esse perfil?",
        "Esse cliente Prime pode evoluir para Principal?",
        "Faça um resumo CRM consultivo do cliente.",
        "Recebi um link suspeito para liberar meu cartão. O que faço?",
        "Você consegue ver meus investimentos em outros bancos?",
        "Qual limite esse cliente teria aprovado?",
    ]

    col_a, col_b = st.columns([2, 1])
    with col_b:
        st.markdown("#### Perguntas rápidas")
        for i, example in enumerate(examples):
            if st.button(example, key=f"example_{i}"):
                st.session_state["chat_input"] = example

    with col_a:
        default_question = st.session_state.get("chat_input", "Qual cartão tem maior aderência para esse perfil?")
        question = st.text_area("Mensagem do usuário", value=default_question, height=100)

        if st.button("Perguntar para a Ada", type="primary"):
            response = generate_response(
                question,
                selected_profile=profile,
                nba_df=nba_df,
                products=products,
                system_prompt=build_master_prompt(),
                use_llm=llm_settings.get("use_llm", False),
                llm_provider=llm_settings.get("provider", "mock"),
                llm_model=llm_settings.get("model"),
            )

            if response["blocked"]:
                st.error(response["answer"])
            else:
                st.success("Resposta gerada com segurança")
                st.markdown(response["answer"])

            with st.expander("Detalhes técnicos da resposta"):
                st.json(
                    {
                        "intent": response["intent"],
                        "confidence": response["confidence"],
                        "blocked": response["blocked"],
                        "persona_id": profile.get("persona_id"),
                        "used_llm": response.get("used_llm"),
                        "llm_provider": response.get("llm_provider"),
                        "llm_model": response.get("llm_model"),
                        "llm_ok": response.get("llm_ok"),
                        "llm_error": response.get("llm_error"),
                    }
                )


def tab_profile_360(profile: dict, historico: pd.DataFrame, nba_df: pd.DataFrame):
    st.subheader("👤 Visão 360º do Cliente Mockado")
    snapshot = calculate_financial_snapshot(profile)
    rec = recommend_card_from_profile(profile)
    nba = get_client_nba(nba_df, profile.get("persona_id", ""))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Segmento", profile.get("segmento_atual", "-"))
    m2.metric("Temperatura", profile.get("temperatura_lead", "-"))
    m3.metric("Score potencial", profile.get("score_potencial_principal_mock", "-"))
    m4.metric("Cartão recomendado", rec.card)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Patrimônio investível mock", money(snapshot["patrimonio_investivel"]))
    c2.metric("Investimentos Bradesco mock", money(snapshot["investimentos_bradesco"]))
    c3.metric("Share wallet mock", pct(snapshot["share_wallet"]))
    c4.metric("Gasto cartão mock", money(snapshot["gasto_cartao"]))

    st.markdown("### Resumo consultivo")
    st.markdown(summarize_profile(profile, nba))

    st.markdown("### Evolução histórica 12 meses")
    hist = get_client_history(historico, profile.get("persona_id", ""))
    if hist.empty:
        st.warning("Sem histórico para a persona selecionada.")
    else:
        chart_data = hist.copy()
        for col in ["renda_mensal_mock", "investimentos_bradesco_mock", "gasto_cartao_mock"]:
            if col in chart_data:
                chart_data[col] = pd.to_numeric(chart_data[col], errors="coerce").fillna(0)
        chart_data = chart_data.set_index("competencia")
        st.line_chart(chart_data[["renda_mensal_mock", "investimentos_bradesco_mock", "gasto_cartao_mock"]])

        with st.expander("Ver histórico detalhado"):
            st.dataframe(hist, use_container_width=True)


def tab_recommendation_simulator():
    st.subheader("🧭 Simulador de Recomendação por Aderência")
    st.write("Simule uma recomendação sem usar dados reais.")

    c1, c2, c3 = st.columns(3)
    with c1:
        segmento = st.selectbox("Segmento atual", ["Principal", "Prime"])
        viagens = st.slider("Viagens internacionais por ano", 0, 12, 4)
    with c2:
        gasto = st.slider("Gasto mensal estimado no cartão", 1000, 80000, 18000, step=1000)
        patrimonio = st.slider("Patrimônio investível mock", 0, 10000000, 1200000, step=100000)
    with c3:
        sala_vip = st.selectbox("Interesse em salas VIP", ["Baixa", "Média", "Alta"], index=2)
        pontos = st.selectbox("Interesse em pontos/milhas", ["Baixa", "Média", "Alta"], index=2)

    prioridade = st.selectbox(
        "Prioridade principal",
        [
            "equilíbrio entre pontos e benefícios",
            "viagem internacional e salas VIP",
            "experiências premium e lifestyle",
            "isenção de anuidade e relacionamento",
            "segurança digital e praticidade",
        ],
    )

    rec = recommend_card_from_inputs(
        viagens_ano=viagens,
        gasto_mensal=gasto,
        interesse_sala_vip=sala_vip,
        interesse_pontos=pontos,
        prioridade=prioridade,
        segmento_atual=segmento,
        patrimonio_investivel=patrimonio,
    )

    st.markdown("### Resultado")
    r1, r2, r3 = st.columns(3)
    r1.metric("Cartão com maior aderência", rec.card)
    r2.metric("Score consultivo", f"{rec.score}/100")
    r3.metric("Segmento", segmento)

    st.markdown(f"**Justificativa:** {rec.rationale}")
    st.markdown(f"**Próximo passo:** {rec.next_step}")
    st.warning(rec.guardrail)


def tab_crm_dashboard(clientes: pd.DataFrame, historico: pd.DataFrame, nba: pd.DataFrame):
    st.subheader("📊 Dashboard CRM e Data-Driven Banking")
    resumo = summarize_dataset(clientes, historico, nba)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Personas", resumo["total_clientes"])
    c2.metric("Principal", resumo["principal"])
    c3.metric("Prime potencial", resumo["prime"])
    c4.metric("Histórico 12m", resumo["historico_registros"])

    c5, c6, c7 = st.columns(3)
    c5.metric("Patrimônio investível mock", money(resumo.get("patrimonio_total_mock", 0)))
    c6.metric("Aporte previsto mock", money(resumo.get("aporte_previsto_mock", 0)))
    c7.metric("NBA registros", resumo["nba_registros"])

    st.markdown("### Distribuição por temperatura")
    if "temperatura_lead" in clientes.columns:
        st.bar_chart(clientes["temperatura_lead"].value_counts())

    st.markdown("### Distribuição por segmento psicológico financeiro")
    if "segmentacao_psicologica_mock" in clientes.columns:
        st.bar_chart(clientes["segmentacao_psicologica_mock"].value_counts().head(10))

    st.markdown("### Base de clientes mockados")
    important_cols = [
        "persona_id", "nome_ficticio", "segmento_atual", "temperatura_lead",
        "score_potencial_principal_mock", "segmentacao_psicologica_mock",
        "cartao_recomendado_ada", "proximo_passo_sugerido"
    ]
    cols = [c for c in important_cols if c in clientes.columns]
    st.dataframe(clientes[cols], use_container_width=True)


def tab_nba(nba: pd.DataFrame, profile: dict):
    st.subheader("🎯 Next Best Action")
    st.write("Motor prescritivo mockado para orientar a próxima ação consultiva.")

    persona_id = profile.get("persona_id", "")
    selected = nba[nba["persona_id"] == persona_id] if "persona_id" in nba else pd.DataFrame()

    if not selected.empty:
        row = selected.iloc[0].to_dict()
        c1, c2, c3 = st.columns(3)
        c1.metric("Ação", row.get("next_best_action_mock", "-"))
        c2.metric("Produto/Tema", row.get("produto_ou_tema_prioritario", "-"))
        c3.metric("Urgência", row.get("urgencia", "-"))

        st.markdown(f"**Canal prescritivo:** {row.get('melhor_canal_prescritivo_mock', '-')}")
        st.markdown(f"**Motivo:** {row.get('motivo_nba', '-')}")
        st.info(row.get("mensagem_consultiva_sugerida", ""))
        st.warning(row.get("guardrail", "Recomendação mockada. Validar em canais oficiais."))

    st.markdown("### Todas as ações")
    st.dataframe(nba, use_container_width=True)


def tab_security_lab():
    st.subheader("🛡️ Laboratório de Segurança e Guardrails")
    st.write("Teste como a Ada bloqueia dados sensíveis e pedidos fora do escopo.")

    samples = [
        "Meu CPF é 123.456.789-09, veja se tenho limite.",
        "Meu cartão é 4111 1111 1111 1111.",
        "Minha senha é 1234.",
        "Qual cartão combina para quem viaja muito?",
        "Recebi um link suspeito pedindo CVV.",
    ]

    sample = st.selectbox("Exemplo", samples)
    custom = st.text_area("Mensagem para validar", value=sample, height=90)

    ok, refusal = validate_user_message(custom)
    if ok:
        st.success("Mensagem permitida pela camada de segurança.")
        st.write("A Ada pode seguir para diagnóstico ou resposta consultiva.")
    else:
        st.error("Mensagem bloqueada por conter dado sensível ou pedido inseguro.")
        st.markdown(refusal)

    st.markdown("### Guardrails carregados")
    prompts = cached_prompts()
    guardrail_keys = [k for k in prompts if "guardrail" in k or "seguranca" in k or "privacidade" in k]
    st.json({"guardrails": guardrail_keys, "total_prompts": len(prompts)})


def tab_prompts():
    st.subheader("🧠 Prompt Center")
    prompts = cached_prompts()

    st.metric("Prompts carregados", len(prompts))
    selected = st.selectbox("Arquivo de prompt", list(prompts.keys()))
    st.code(prompts[selected][:6000], language="markdown")

    with st.expander("Master prompt consolidado"):
        master = build_master_prompt()
        st.write(f"Caracteres: {len(master)}")
        st.code(master[:8000], language="markdown")



def tab_llm_compatibility():
    st.subheader("🤖 Compatibilidade Multi-LLM")
    st.write("A Ada pode operar em modo local determinístico ou chamar uma LLM externa por adaptadores.")

    status = get_provider_status()
    rows = []
    for provider, info in status.items():
        rows.append(
            {
                "provider": provider,
                "ready": info.get("ready"),
                "env_vars": ", ".join(info.get("env", [])),
                "description": info.get("description"),
                "default_model": DEFAULT_MODELS.get(provider),
            }
        )

    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.markdown(
        """
### Como usar

1. Mantenha `mock` para demonstração sem chave de API.
2. Para OpenAI/ChatGPT, configure `OPENAI_API_KEY`.
3. Para Gemini, configure `GEMINI_API_KEY`.
4. Para Claude, configure `ANTHROPIC_API_KEY`.
5. Para Qwen, configure `QWEN_API_KEY` ou `DASHSCOPE_API_KEY`.
6. Nunca coloque chaves no GitHub. Use variáveis de ambiente ou arquivo `.env` local não versionado.

### Comportamento esperado

- O motor determinístico aplica segurança antes de qualquer chamada externa.
- A LLM recebe apenas contexto mockado e resposta segura inicial.
- A saída da LLM passa por guardrail de pós-processamento.
- Se a LLM falhar, a Ada usa fallback local seguro.
"""
    )


def tab_evaluation_metrics():
    st.subheader("📈 Avaliação & Métricas Nota 10")
    st.write("Painel executivo com resultados da suíte de avaliação automatizada da Ada.")

    report_path = ROOT / "reports" / "evaluation_report.json"
    scores_path = ROOT / "reports" / "evaluation_scores_1_10.csv"
    metrics_path = ROOT / "reports" / "advanced_metrics.csv"

    if not report_path.exists():
        st.warning("Relatório ainda não encontrado. Execute `python scripts/run_evaluation.py` para gerar as métricas.")
        return

    report = json.loads(report_path.read_text(encoding="utf-8"))
    summary = report.get("summary", {})
    advanced = report.get("advanced_metrics", {})

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Taxa geral", f"{summary.get('overall_pass_rate', 0):.0%}")
    c2.metric("Segurança", f"{summary.get('safety_pass_rate', 0):.0%}")
    c3.metric("Casos críticos", f"{summary.get('critical_pass_rate', 0):.0%}")
    c4.metric("Recomendação", f"{summary.get('recommendation_accuracy', 0):.0%}")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Nota média", f"{summary.get('nota_media_1_10', 0):.2f}/10")
    c6.metric("Nota mínima", f"{summary.get('nota_minima_1_10', 0)}/10")
    c7.metric("Notas 10", f"{summary.get('taxa_nota_10', 0):.0%}")
    c8.metric("Unsafe output", f"{summary.get('unsafe_output_rate', 0):.0%}")

    if summary.get("approved"):
        st.success("Status: APROVADO — a suíte atingiu a régua nota 10.")
    else:
        st.error("Status: REVISAR — alguma métrica ficou abaixo da régua.")

    st.markdown("### Métricas avançadas")
    metrics_table = []
    for key, value in advanced.items():
        if key != "base_summary_reference":
            metrics_table.append({"métrica": key, "valor": value})
    if metrics_table:
        st.dataframe(pd.DataFrame(metrics_table), use_container_width=True)

    st.markdown("### Solicitações avaliadas de 1 a 10")
    if scores_path.exists():
        scores = pd.read_csv(scores_path)
        cols = [c for c in ["case_id", "categoria", "grade_1_10", "meets_user_quality_bar", "latency_ms", "estimated_total_tokens"] if c in scores.columns]
        st.dataframe(scores[cols], use_container_width=True)
        st.bar_chart(scores.set_index("case_id")["grade_1_10"])

    st.markdown("### Casos funcionais e críticos")
    results = report.get("general_results", []) + report.get("critical_results", [])
    if results:
        results_df = pd.DataFrame(results)
        cols = [c for c in ["case_id", "categoria", "passed", "score", "intent_actual", "blocked_actual"] if c in results_df.columns]
        st.dataframe(results_df[cols], use_container_width=True)

    st.caption("Os dados são mockados e a avaliação é educacional. Em produção, métricas devem ser conectadas a logs, observabilidade e governança reais.")

def main():
    core = cached_core_data()
    crm = cached_crm_data()

    clientes = crm["clientes"]
    historico = crm["historico_12m"]
    nba = crm["next_best_action"]

    render_header()
    profile, llm_settings = render_sidebar(clientes)

    tabs = st.tabs(
        [
            "Chat Ada",
            "Cliente 360",
            "Simulador",
            "CRM Dashboard",
            "Next Best Action",
            "Segurança",
            "Prompts",
            "Multi-LLM",
            "Avaliação & Métricas",
        ]
    )

    with tabs[0]:
        tab_chat(profile, nba, core.get("produtos", []), llm_settings)
    with tabs[1]:
        tab_profile_360(profile, historico, nba)
    with tabs[2]:
        tab_recommendation_simulator()
    with tabs[3]:
        tab_crm_dashboard(clientes, historico, nba)
    with tabs[4]:
        tab_nba(nba, profile)
    with tabs[5]:
        tab_security_lab()
    with tabs[6]:
        tab_prompts()
    with tabs[7]:
        tab_llm_compatibility()
    with tabs[8]:
        tab_evaluation_metrics()


if __name__ == "__main__":
    main()
