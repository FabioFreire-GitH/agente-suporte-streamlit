import sys
import os

# Adiciona o diretório 'src' ao path do Python para encontrar o pacote 'agente_suporte'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import streamlit as st
from agente_suporte.agente import criar_agente_suporte

# ─────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Agente de Suporte",
    page_icon="🤖",
    layout="centered",
)

# ─────────────────────────────────────────────
# URLs de cada sistema (edite aqui para adicionar páginas)
# ─────────────────────────────────────────────
URLS_MOUB = [
    "https://ajuda.moub.com.br/guia/",
    "https://ajuda.moub.com.br/guia/produtos.html",
    "https://ajuda.moub.com.br/guia/primeiros-passos.html",
    "https://ajuda.moub.com.br/guia/dashboard.html",
    "https://ajuda.moub.com.br/guia/cadastros/administradores.html",
    "https://ajuda.moub.com.br/guia/cadastros/usuarios.html",
    "https://ajuda.moub.com.br/guia/cadastros/gestores.html",
    "https://ajuda.moub.com.br/guia/cadastros/convenios.html",
    "https://ajuda.moub.com.br/guia/cadastros/beneficiarios.html",
    "https://ajuda.moub.com.br/guia/cadastros/estabelecimentos.html",
    # "https://ajuda.moub.com.br/guia/conta/perfil.html",
    # "https://ajuda.moub.com.br/guia/conta/acesso-e-seguranca.html",
    # "https://ajuda.moub.com.br/guia/conta/configuracoes.html",
    # "https://ajuda.moub.com.br/guia/conta/auditoria.html",
    # "https://ajuda.moub.com.br/guia/papeis-e-permissoes.html",
    # "https://ajuda.moub.com.br/guia/notificacoes.html",
    # "https://ajuda.moub.com.br/guia/monitoramento.html",
    # "https://ajuda.moub.com.br/guia/novidades.html",
    # "https://ajuda.moub.com.br/debito-credito/relatorios/",
    # "https://ajuda.moub.com.br/debito-credito/relatorios/movimentacao.html",
    # "https://ajuda.moub.com.br/debito-credito/relatorios/historico-movimentacao.html",
    # "https://ajuda.moub.com.br/debito-credito/relatorios/saldos.html",
    # "https://ajuda.moub.com.br/debito-credito/relatorios/saldo-custodia.html"
    # "https://ajuda.moub.com.br/debito-credito/relatorios/extrato.html",
    # "https://ajuda.moub.com.br/debito-credito/relatorios/desconto-folha.html",
    # "https://ajuda.moub.com.br/debito-credito/relatorios/vencimento-cartao.html",
    # "https://ajuda.moub.com.br/debito-credito/relatorios/carteira-convenios.html",
    # "https://ajuda.moub.com.br/debito-credito/relatorios/quadro-beneficiarios.html",
    # "https://ajuda.moub.com.br/debito-credito/ferramentas/novo-cartao.html",
    # "https://ajuda.moub.com.br/debito-credito/ferramentas/imprimir-cartao.html"
    # "https://ajuda.moub.com.br/fidelidade/",
    # "https://ajuda.moub.com.br/fidelidade/pontuacao.html",
    # "https://ajuda.moub.com.br/fidelidade/premios.html"
    # "https://ajuda.moub.com.br/fidelidade/acesso-do-convenio.html",
    # "https://ajuda.moub.com.br/fidelidade/dashboard.html",
    # "https://ajuda.moub.com.br/fidelidade/operacao/pontuar.html",
    # "https://ajuda.moub.com.br/fidelidade/operacao/estornos.html",
    # "https://ajuda.moub.com.br/fidelidade/relatorios/extrato-pontos.html",
    # "https://ajuda.moub.com.br/fidelidade/relatorios/resgates.html",
    # "https://ajuda.moub.com.br/fidelidade/relatorios/fidelizacao-por-dia.html",
]

URLS_BLUVE = [
    "https://ajuda.bluve.com.br/",
    "https://ajuda.bluve.com.br/guia/",
    "https://ajuda.bluve.com.br/guia/primeiros-passos.html",
    "https://ajuda.bluve.com.br/guia/dashboard.html",
    "https://ajuda.bluve.com.br/guia/monitoramento.html",
    "https://ajuda.bluve.com.br/guia/cadastros/lojas.html",
]

# ─────────────────────────────────────────────
# Cache: carrega os agentes apenas uma vez
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner="⏳ Carregando agente MOUB...")
def carregar_agente_moub():
    return criar_agente_suporte(
        nome_sistema="moub",
        urls_documentacao=URLS_MOUB,
        recriar_banco=False,  # Mude para True para forçar atualização do banco
    )

@st.cache_resource(show_spinner="⏳ Carregando agente BLUVE...")
def carregar_agente_bluve():
    return criar_agente_suporte(
        nome_sistema="bluve",
        urls_documentacao=URLS_BLUVE,
        recriar_banco=False,  # Mude para True para forçar atualização do banco
    )

# ─────────────────────────────────────────────
# Sidebar: seleção do sistema
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("🤖 Agente de Suporte")
    st.divider()

    sistema = st.selectbox(
        "Selecione o sistema:",
        options=["MOUB", "BLUVE"],
        index=0,
    )

    st.divider()
    if st.button("🗑️ Limpar conversa", use_container_width=True):
        st.session_state.historico = []
        st.rerun()

    st.caption("Os agentes respondem com base na documentação oficial de cada sistema.")

# ─────────────────────────────────────────────
# Carrega o agente do sistema selecionado
# ─────────────────────────────────────────────
if sistema == "MOUB":
    agente = carregar_agente_moub()
else:
    agente = carregar_agente_bluve()

# ─────────────────────────────────────────────
# Estado da sessão: histórico de mensagens
# ─────────────────────────────────────────────
if "historico" not in st.session_state:
    st.session_state.historico = []

# Limpa o histórico ao trocar de sistema
if "sistema_atual" not in st.session_state:
    st.session_state.sistema_atual = sistema

if st.session_state.sistema_atual != sistema:
    st.session_state.historico = []
    st.session_state.sistema_atual = sistema

# ─────────────────────────────────────────────
# Cabeçalho principal
# ─────────────────────────────────────────────
st.title(f"Suporte {sistema}")
st.caption(f"Tire suas dúvidas sobre o sistema **{sistema}**. As respostas são baseadas na documentação oficial.")

# ─────────────────────────────────────────────
# Exibe histórico de mensagens
# ─────────────────────────────────────────────
for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────
# Input do usuário
# ─────────────────────────────────────────────
pergunta = st.chat_input(f"Pergunte algo sobre o {sistema}...")

if pergunta:
    # Exibe a mensagem do usuário
    st.session_state.historico.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Chama o agente e exibe a resposta
    with st.chat_message("assistant"):
        with st.spinner("Consultando a documentação..."):
            resposta = agente.run(pergunta)
            texto_resposta = resposta.content

        st.markdown(texto_resposta)

    st.session_state.historico.append({"role": "assistant", "content": texto_resposta})
