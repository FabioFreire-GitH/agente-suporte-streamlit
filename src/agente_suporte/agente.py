import os
import shutil 
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.firecrawl_reader import FirecrawlReader
from agno.knowledge.chunking.recursive import RecursiveChunking
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.vectordb.chroma import ChromaDb

load_dotenv()

def criar_agente_suporte(nome_sistema: str, urls_documentacao: list, recriar_banco: bool = False) -> Agent:
    """
    Cria um agente isolado para um sistema específico.
    Se recriar_banco for True, ele apaga a pasta física do banco e baixa tudo do zero.
    """
    
    caminho_sqlite = f"tmp/chat_{nome_sistema}.db"
    caminho_chroma = f"tmp/chroma_{nome_sistema}"
    nome_colecao = f"docs_{nome_sistema}"

    # 1. Limpeza Física Brutal (Se solicitado)
    if recriar_banco and os.path.exists(caminho_chroma):
        print(f"🧹 [{nome_sistema.upper()}] Deletando a pasta física do banco antigo...")
        shutil.rmtree(caminho_chroma, ignore_errors=True)
    
    # 2. Banco de memória específico do sistema
    db = SqliteDb(db_file=caminho_sqlite)

    # 3. Vector DB (Agora ele recria a pasta sozinho se a gente deletou)
    vector_db = ChromaDb(
        collection=nome_colecao,
        path=caminho_chroma, 
        embedder=GeminiEmbedder(api_key=os.getenv("GOOGLE_API_KEY")),
        persistent_client=True,
    )

    # 4. Leitor web
    firecrawl_reader = FirecrawlReader(
        api_key=os.getenv("FIRECRAWL_API_KEY"),
        mode="scrape",
        chunking_strategy=RecursiveChunking(
            chunk_size=1500,
            overlap=200,
        ),
    )

    knowledge = Knowledge(vector_db=vector_db)

    # 5. Checagem do tamanho do banco
    tamanho_banco = 0
    try:
        tamanho_banco = vector_db.get_count()
    except Exception:
        pass

    # 6. Lógica de Inserção Real
    if tamanho_banco == 0 or recriar_banco:
        print(f"🤖 [{nome_sistema.upper()}] Iniciando a leitura e vetorização do manual...")
        for url in urls_documentacao:
            print(f"📥 [{nome_sistema.upper()}] Baixando: {url}")
            try:
                # knowledge.insert gerencia internamente o chunking e os IDs únicos por chunk
                knowledge.insert(url=url, reader=firecrawl_reader, upsert=True)
                print(f"✅ Inserido no banco de dados!")
            except Exception as e:
                print(f"❌ Erro ao processar {url}: {e}")
                
        print(f"📊 [{nome_sistema.upper()}] Sucesso! Total de pedaços salvos: {vector_db.get_count()}")
    else:
        print(f"🚀 [{nome_sistema.upper()}] Banco já contém {tamanho_banco} blocos de texto! Carregando agente...")

    # 7. Construção do Agente
    instrucoes = f"""Você é um assistente de suporte técnico focado em ajudar usuários do sistema {nome_sistema.upper()}. 
    Responda SEMPRE baseando-se na documentação fornecida. Se a resposta não estiver na base, diga educadamente 
    que essa informação não consta no manual do {nome_sistema.upper()}."""

    agente = Agent(
        name=f"suporte_{nome_sistema}",
        model=Gemini(id="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY")),
        instructions=instrucoes,
        db=db,
        add_history_to_context=True,
        enable_user_memories=True,
        knowledge=knowledge,
        search_knowledge=True,
        num_history_messages=5,
    )

    return agente