from database import supabase

def ver_pedidos_pendentes():
    print("\n" + "="*15 + " 🍳 PEDIDOS PARA PREPARAR " + "="*15)
    try:
        # Busca pedidos com status 'Pago - Preparando' na tabela vendas
        resposta = supabase.table("vendas").select("*").eq("status", "Pago - Preparando").execute()
        pedidos = resposta.data

        if not pedidos:
            print("✅ Não há pedidos pendentes para preparo no momento.")
        else:
            print(f"{'ID':<6}| {'RM CLIENTE':<12}| {'VALOR':<10}| {'COD. RETIRADA':<10}")
            print("-" * 55)
            for p in pedidos:
                print(f"{p['id_pedido']:<6}| {p['rm']:<12}| R$ {p['valor']:>6.2f}| {p['codigo_retirada']:<10}")
    except Exception as e:
        print(f"❌ Erro ao buscar pedidos: {e}")
    
    input("\nPressione Enter para voltar ao menu...")

def marcar_como_pronto():
    while True:
        print("\n" + "="*15 + " ✅ FINALIZAR PREPARO " + "="*15)
        try:
            # Lista os que estão sendo preparados para o cozinheiro escolher
            resposta = supabase.table("vendas").select("*").eq("status", "Pago - Preparando").execute()
            pedidos = resposta.data
            
            if not pedidos:
                print("⚠️ Nenhum pedido pendente no momento.")
                input("\nPressione Enter para voltar ao menu...")
                break
            else:
                print(f"{'ID':<6}| {'RM':<12}| {'CÓDIGO':<10}")
                print("-" * 35)
                for p in pedidos:
                    print(f"{p['id_pedido']:<6}| {p['rm']:<12}| {p['codigo_retirada']:<10}")
                
                id_input = input("\nDigite o ID do pedido que está PRONTO (ou '0' para cancelar): ").strip()
                
                if id_input == '0':
                    break
                    
                if not id_input or not id_input.isdigit():
                    print("❌ Erro: Digite um número de ID válido.")
                else:
                    # Atualiza o status para retirada
                    supabase.table("vendas").update({"status": "Pronto para Retirada"}).eq("id_pedido", int(id_input)).execute()
                    print(f"✅ Sucesso! Pedido {id_input} movido para retirada.")
                
                # Pergunta se deseja continuar marcando outros
                continuar = input("\nDeseja marcar outro pedido como pronto? (s/n): ").lower()
                if continuar != 's':
                    break
                
        except Exception as e:
            print(f"❌ Erro ao atualizar status: {e}")
            break

def menu_restaurante():
    """Função principal chamada pelo fazer_login.py"""
    while True:
        print('\n' + '='*15 + ' 👨‍🍳 PAINEL DA COZINHA ' + '='*15)
        print('1 - Ver Pedidos Pendentes')
        print('2 - Marcar Pedido como PRONTO')
        print('3 - Sair (Logout)')
        
        opcao = input('\nEscolha uma operação: ')

        if opcao == '1':
            ver_pedidos_pendentes()
        elif opcao == '2':
            marcar_como_pronto()
        elif opcao == '3':
            print("Saindo do sistema da cozinha...")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu_restaurante()