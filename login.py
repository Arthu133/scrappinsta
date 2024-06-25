import instaloader
import os

# Criar uma instância do Instaloader
L = instaloader.Instaloader()

# Pegar as credenciais das variáveis de ambiente
username = os.getenv('celtacruel')
password = os.getenv('Girafa:123')

try:
    L.login(username, password)
    L.save_session_to_file()
    print(f"Login realizado e sessão salva para o usuário {username}.")
except instaloader.exceptions.TwoFactorAuthRequiredException:
    print("Autenticação de dois fatores é necessária.")
    two_factor_code = input("Digite o código de autenticação de dois fatores: ")
    L.two_factor_login(two_factor_code)
    L.save_session_to_file()
    print(f"Login com 2FA realizado e sessão salva para o usuário {username}.")
except instaloader.exceptions.BadCredentialsException:
    print("Erro de login: Nome de usuário ou senha incorretos.")
except instaloader.exceptions.ConnectionException:
    print("Erro de conexão. Tente novamente mais tarde.")
except Exception as e:
    print(f"Erro inesperado: {e}")
