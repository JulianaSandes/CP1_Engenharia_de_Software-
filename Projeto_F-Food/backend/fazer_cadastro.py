from database import supabase

def cadastrar_usuario_grafico(rm, cpf, nome, senha):
    try:
        # Define o perfil automaticamente
        perfil = "Gerente" if "ADMIN" in nome.upper() else "Cliente"
        
        dados = {
            "rm": rm,
            "cpf": cpf,
            "nome": nome,
            "senha": senha,
            "perfil": perfil
        }

        supabase.table("usuarios").insert(dados).execute()
        return True, "Cadastro realizado com sucesso!"
    except Exception as e:
        return False, f"Erro ao cadastrar: {e}"