from database import supabase
import random

def exibir_cardapio(apenas_listar=False):
    print("\n" + "="*15 + " 📋 CARDÁPIO F-FOOD " + "="*15)
    try:
        resposta = supabase.table("cardapio").select("*").execute()
        itens = resposta.data
        if not itens:
            print("⚠️ O cardápio está vazio.")
            return False
        
        print(f"{'ID':<6}| {'NOME':<25}| {'PREÇO':<11}")
        print("-" * 45)
        for item in itens:
            print(f"{item['id']:<6}| {item['nome']:<25}| R$ {item['preco']:>7.2f}")
        
        if not apenas_listar:
            input("\nPressione Enter para voltar...")
        return True
    except Exception as e:
        print(f"❌ Erro ao ler cardápio: {e}")
        return False

def f_pagamento(rm_usuario):
    print("\n" + "="*10 + " 💳 FINALIZAÇÃO E PAGAMENTO " + "="*10)
    try:
        # Busca os pedidos que estão "Aguardando Pagamento" para este RM
        resposta = supabase.table("vendas").select("*").eq("rm", rm_usuario).eq("status", "Aguardando Pagamento").execute()
        pedidos = resposta.data

        if not pedidos:
            print("⚠️ Você não tem pedidos pendentes no carrinho.")
            input("\nPressione Enter para voltar...")
            return

        total = sum(p['valor'] for p in pedidos)
        print(f"Total a pagar: R$ {total:.2f}")
        print("\n1 - Cartão de Crédito\n2 - Cartão de Débito\n3 - PIX")
        
        metodo = input("Selecione o método de pagamento: ")
        print("Processando...")
        
        # Atualiza todos os pedidos pendentes para "Pago" e "Preparando"
        for p in pedidos:
            supabase.table("vendas").update({"status": "Pago - Preparando"}).eq("id_pedido", p['id_pedido']).execute()
        
        print(f"\n✅ Pagamento realizado com sucesso!")
        print(f"Siga para o balcão com seu RM: {rm_usuario}")
        
    except Exception as e:
        print(f"❌ Erro no pagamento: {e}")
    
    input("\nPressione Enter para voltar ao menu...")

def fazer_pedido(rm_usuario):
    while True:
        print("\n--- 🛒 ADICIONAR AO PEDIDO ---")
        if not exibir_cardapio(apenas_listar=True):
            break

        try:
            id_item = input("\nDigite o ID do item (ou '0' para cancelar): ").strip()
            if id_item == '0': break

            quantidade = int(input("Quantidade: "))
            item_query = supabase.table("cardapio").select("*").eq("id", id_item).execute()
            
            if item_query.data:
                item = item_query.data[0]
                valor_total = item['preco'] * quantidade
                cod_retirada = f"FF-{random.randint(100, 999)}"

                dados_venda = {
                    "rm": rm_usuario,
                    "valor": valor_total,
                    "status": "Aguardando Pagamento",
                    "codigo_retirada": cod_retirada
                }

                supabase.table("vendas").insert(dados_venda).execute()
                print(f"\n✅ {quantidade}x {item['nome']} adicionado!")
                
                continuar = input("\nDeseja adicionar outro item? (s/n): ").lower()
                if continuar != 's':
                    # AQUI ESTÁ A MUDANÇA: Se 'n', ele chama o pagamento direto
                    print("\nRedirecionando para o pagamento...")
                    f_pagamento(rm_usuario)
                    break
            else:
                print("❌ ID não encontrado.")
        except Exception as e:
            print(f"❌ Erro: {e}")
            break

def consultar_status_pedido(rm_usuario):
    print("\n--- 🔍 MEUS PEDIDOS ---")
    try:
        resposta = supabase.table("vendas").select("*").eq("rm", rm_usuario).execute()
        pedidos = resposta.data
        if not pedidos:
            print("Nenhum pedido encontrado.")
        else:
            print(f"{'ID':<6}| {'VALOR':<10}| {'STATUS':<20}| {'CÓDIGO':<8}")
            print("-" * 50)
            for p in pedidos:
                print(f"{p['id_pedido']:<6}| R$ {p['valor']:>6.2f}| {p['status']:<20}| {p['codigo_retirada']:<8}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    input("\nPressione Enter para voltar...")

def menu_cliente(rm_usuario):
    while True:
        print('\n' + '='*15 + f' MENU F-FOOD (RM: {rm_usuario}) ' + '='*15)
        print('1 - Ver Cardápio')
        print('2 - Fazer Pedido')
        print('3 - Finalizar Pendentes/Pagar')
        print('4 - Ver Status/Retirar Pedido')
        print('5 - Sair (Logout)')

        n = input('Digite a opção desejada: ')

        if n == '1':
            exibir_cardapio()
        elif n == '2':
            fazer_pedido(rm_usuario)
        elif n == '3':
            f_pagamento(rm_usuario)
        elif n == '4':
            consultar_status_pedido(rm_usuario)
        elif n == '5':
            break
        else:
            print('❌ Opção inválida!')