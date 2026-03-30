from database import supabase

def listar_simples():
    """Função auxiliar para mostrar os itens antes de pedir o ID"""
    try:
        resposta = supabase.table("cardapio").select("*").execute()
        itens = resposta.data
        if not itens:
            print("⚠️ Cardápio vazio.")
            return False
        
        print(f"\n{'ID':<6}| {'NOME':<25}| {'PREÇO':<11}| {'ESTOQUE':<8}")
        print("-" * 55)
        for item in itens:
            print(f"{item['id']:<6}| {item['nome']:<25}| R$ {item['preco']:>7.2f}| {item['estoque']:>7}")
        return True
    except Exception as e:
        print(f"❌ Erro ao listar: {e}")
        return False

def visualizar_estoque():
    print("\n--- 📋 ESTOQUE ATUAL ---")
    listar_simples()
    input("\nPressione Enter para voltar...")

def cadastrar_item():
    print("\n--- CADASTRAR NOVO ITEM ---")
    nome = input("Nome do prato/bebida: ").strip()
    preco = float(input("Preço: ").replace(',', '.'))
    estoque = int(input("Quantidade em estoque: "))
    
    try:
        supabase.table("cardapio").insert({
            "nome": nome, 
            "preco": preco, 
            "estoque": estoque
        }).execute()
        print(f"✅ {nome} cadastrado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")
    input("\nPressione Enter...")

def excluir_item():
    print("\n--- EXCLUIR ITEM ---")
    if listar_simples():
        id_item = input("\nDigite o ID do item que deseja REMOVER: ")
        try:
            supabase.table("cardapio").delete().eq("id", id_item).execute()
            print(f"🗑️ Item ID {id_item} removido!")
        except Exception as e:
            print(f"❌ Erro ao excluir: {e}")
    input("\nPressione Enter...")

def alterar_item(coluna):
    print(f"\n--- ALTERAR {coluna.upper()} ---")
    if listar_simples():
        id_item = input(f"\nDigite o ID do item para ajustar {coluna}: ")
        novo_valor = input(f"Digite o novo valor para {coluna}: ").replace(',', '.')
        
        try:
            val = float(novo_valor) if coluna == 'preco' else int(novo_valor)
            supabase.table("cardapio").update({coluna: val}).eq("id", id_item).execute()
            print(f"✅ {coluna.capitalize()} atualizado!")
        except Exception as e:
            print(f"❌ Erro ao atualizar: {e}")
    input("\nPressione Enter...")

def menu_gerente():
    while True:
        print('\n--- ⚙️ PAINEL DE CONTROLE (GERENTE) ---')
        print('1 - Visualizar Estoque')
        print('2 - Cadastrar Novo Item')
        print('3 - Excluir Item')
        print('4 - Alterar Preço')
        print('5 - Ajustar Estoque')
        print('6 - Sair (Logout)')

        opcao = input('Selecione a operação: ')

        if opcao == '1':
            visualizar_estoque()
        elif opcao == '2':
            cadastrar_item()
        elif opcao == '3':
            excluir_item()
        elif opcao == '4':
            alterar_item('preco')
        elif opcao == '5':
            alterar_item('estoque')
        elif opcao == '6':
            break
        else:
            print("❌ Opção inválida!")