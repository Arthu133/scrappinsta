import instaloader


# Função para obter seguidores de um perfil
def get_followers(username):
    try:
        # Carregando o perfil desejado
        profile = instaloader.Profile.from_username(loader.context, username)

        # Obtendo o número de seguidores
        followers = profile.followers

        return followers
 
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"O perfil @{username} não existe.")
    except Exception as e: 
        print(f"Ocorreu um erro ao obter seguidores do @{username}: {e}")
        return None
 
# Abrindo o arquivo com os usernames 
filename = 'cristiano_followers.txt' 

# Lista para armazenar os usernames do arquivo
usernames = []

# Lendo os usernames do arquivo
with open(filename, 'r') as file:
    for line in file:
        usernames.append(line.strip())

# Criando uma instância do Instaloader
loader = instaloader.Instaloader()

# Abrindo o arquivo para escrita dos resultados filtrados
output_filename = 'usuarios.txt'
with open(output_filename, 'w') as output_file:
    # Iterando sobre cada nome de usuário na lista
    for username in usernames:
        followers_count = get_followers(username)
        if followers_count is not None:
            # Filtrando para seguidores entre 10.000 e 150.000
            if 20000 <= followers_count <= 130000:
                output_file.write(f"{username}\n")
                print(f"O perfil @{username} tem {followers_count} seguidores e foi adicionado ao arquivo {output_filename}.")

print(f"Processo concluído! Perfis filtrados foram salvos em {output_filename}.")
