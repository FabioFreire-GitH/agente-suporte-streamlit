from agente_suporte.agente import criar_agente_suporte

def main():
    # 1. Defina as URLs do sistema MOUB
    urls_moub = [
        'https://ajuda.moub.com.br/guia/',
        'https://ajuda.moub.com.br/guia/produtos.html',
        'https://ajuda.moub.com.br/guia/primeiros-passos.html',
        'https://ajuda.moub.com.br/guia/dashboard.html',
        'https://ajuda.moub.com.br/guia/cadastros/administradores.html',
        'https://ajuda.moub.com.br/guia/cadastros/usuarios.html',
        'https://ajuda.moub.com.br/guia/cadastros/gestores.html',
        'https://ajuda.moub.com.br/guia/cadastros/convenios.html',
        'https://ajuda.moub.com.br/guia/cadastros/beneficiarios.html',
        'https://ajuda.moub.com.br/guia/cadastros/estabelecimentos.html',
        # ... outras urls
    ]
    
    # 2. Defina as URLs do sistema BLUVE (quando for testar)
    urls_bluve = [
        'https://ajuda.bluve.com.br/',
        'https://ajuda.bluve.com.br/guia/',
        'https://ajuda.bluve.com.br/guia/primeiros-passos.html',
        'https://ajuda.bluve.com.br/guia/dashboard.html',
        'https://ajuda.bluve.com.br/guia/monitoramento.html',
        'https://ajuda.bluve.com.br/guia/cadastros/lojas.html',
        # ... outras urls
        ]

    # 3. Cria (ou carrega) o agente do Moub
    agente_moub = criar_agente_suporte(nome_sistema="moub", urls_documentacao=urls_moub, recriar_banco=False)  # Mude para True para recriar o banco do zero
    
    agente_bluve = criar_agente_suporte(nome_sistema="bluve", urls_documentacao=urls_bluve, recriar_banco=True)  # Defina como True para recriar o banco

    # 4. Bateria de Testes
    print("\n==============================")
    print("   INICIANDO CHAT DE TESTE    ")
    print("==============================\n")
    
    agente_moub.print_response("O que são Convênios no sistema MOUB e como eles funcionam?")
    agente_moub.print_response("O que são Usuários no sistema MOUB e como eles funcionam?")
    agente_moub.print_response("Em adminstradores, quais as permissões de acesso?")

    agente_bluve.print_response("O que são Lojas no sistema BLUVE e como elas funcionam?")
    agente_bluve.print_response("O que são Usuários no sistema BLUVE e como eles funcionam?")
    agente_bluve.print_response("Em adminstradores, quais as permissões de acesso?")

if __name__ == "__main__":
    main()