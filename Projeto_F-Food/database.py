from supabase import create_client, Client

# Use a URL que você já tinha e essa nova chave que você copiou
URL = "https://rqhfkkmqpdcdissxexob.supabase.co"
KEY = "sb_publishable_n1HnArtu_iL5tJ42hP_cGQ_OlVcXu_b" # Cole a chave completa aqui

supabase: Client = create_client(URL, KEY)