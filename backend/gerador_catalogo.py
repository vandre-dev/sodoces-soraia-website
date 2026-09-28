# BACK-END V1 - SÓDOCES (Catálogo de Produtos)

# 1. Estrutura de Dados: Dicionário onde as chaves são as categorias, 
# e os valores são listas contendo dicionários (os produtos).
catalogo = {
    "Bolos por Kg": [
        {"nome": "Bolo de Leite Ninho", "descricao": "Massa branca fofinha com recheio cremoso de Leite Ninho.", "preco": 88.00},
        {"nome": "Bolo Sensação", "descricao": "Massa de chocolate, recheio de morango e cobertura de chocolate.", "preco": 93.00}
    ],
    "Bolos no Pote": [
        {"nome": "Ninho com Nutella", "descricao": "Camadas intercaladas de creme de ninho, nutella e bolo.", "preco": 15.00},
        {"nome": "Brigadeiro", "descricao": "Bolo de chocolate com muito recheio de brigadeiro tradicional.", "preco": 15.00}
    ],
    "Doces de Encomenda (Cento)": [
        {"nome": "Brigadeiro Tradicional", "descricao": "O clássico brigadeiro feito com chocolate nobre.", "preco": 90.00},
        {"nome": "Beijinho", "descricao": "Doce de coco artesanal com cravo.", "preco": 90.00},
        {"nome": "Kinder Bueno", "descricao": "Docinho premium recheado com creme de avelã branco.", "preco": 130.00}
    ]
}

# 2. Função para exibir o cardápio no terminal
def mostrar_cardapio_terminal():
    print('-' * 40)
    print(f'{"CARDÁPIO SÓDOCES":^40}')
    print('-' * 40)
    
    for categoria, produtos in catalogo.items():
        print(f'\n--- {categoria.upper()} ---')
        for item in produtos:
            # Formatando o preço para ficar com 2 casas decimais (ex: R$ 75.00)
            print(f" > {item['nome']:.<25} R$ {item['preco']:.2f}")

# 3. Função "Ponte" 
def exportar_para_html():
    print("\nGerando blocos HTML para o site...\n")
    
    html_gerado = ""
    
    for categoria, produtos in catalogo.items():
        html_gerado += f"\n<!-- Categoria: {categoria} -->\n"
        html_gerado += f'<div class="categoria-menu">\n'
        html_gerado += f'    <h3>{categoria}</h3>\n'
        
        for item in produtos:
            html_gerado += f'    <div class="produto-item">\n'
            html_gerado += f'        <h4>{item["nome"]}</h4>\n'
            html_gerado += f'        <p>{item["descricao"]}</p>\n'
            html_gerado += f'        <span class="preco">R$ {item["preco"]:.2f}</span>\n'
            html_gerado += f'    </div>\n'
            
        html_gerado += f'</div>\n'
    
    print(html_gerado)
    print("\nCÓPIE O CÓDIGO ACIMA E COLE DENTRO DA <section id='cardapio'> NO SEU ARQUIVO HTML!")


# MENU DE EXECUÇÃO
while True:
    print('\n[1] Ver cardápio no terminal')
    print('[2] Gerar código HTML para o site')
    print('[3] Sair')
    
    opcao = str(input('Escolha uma opção: '))
    
    if opcao == '1':
        mostrar_cardapio_terminal()
    elif opcao == '2':
        exportar_para_html()
    elif opcao == '3':
        print('Encerrando o sistema Sódoces...')
        break
    else:
        print('Opção inválida, tente novamente.')