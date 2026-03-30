from database import supabase

def autenticar_usuario(rm_digitado, senha_digitada):
    try:
        # Busca o usuário no banco pelo RM
        resultado = supabase.table("usuarios").select("*").eq("rm", rm_digitado).execute()

        if not resultado.data:
            return False, None, None, "RM não encontrado!"

        usuario = resultado.data[0]

        # Verifica a senha
        if str(usuario['senha']) == str(senha_digitada):
            return True, usuario['perfil'], usuario['nome'], None
        else:
            return False, None, None, "Senha incorreta!"

    except Exception as e:
        return False, None, None, f"Erro de conexão: {e}"