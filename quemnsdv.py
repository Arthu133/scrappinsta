import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
 
# Atenção: Instale as dependências: pip install -r requirements.txt 
# Verifique se o Selenium está instalado: pip show selenium  
# Atualize o selenium: pip install --upgrade selenium  
# Na linha 79 e 81: 
# os.environ["webdriver.chrome.driver"] = "C:\\webdriver\\chromedriver.exe" # PARA WINDOWS
# os.environ["webdriver.chrome.driver"] = "/usr/local/bin/chromedriver"     # PARA MAC
    #coloque o caminho onde está o chromedriver em sua máquina. 
   
def login(driver, login_url, username, password):               
    driver.get(login_url)
    try:
        # Aguarde o formulário de login estar presente na página
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]')))
        
        # Procura o elemento de entrada do nome de usuário e preencha com o nome de usuário
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]//input[@name="username"]')))
        email_input.send_keys(username)

        # Procura o elemento de entrada de senha e preencha com a senha
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]//input[@name="password"]')))
        password_input.send_keys(password)
        
        # Encontra o botão enviar e clique nele
        submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]//button[@type="submit"]')))
        submit.click()

        # Aguarde a conclusão do login (você pode aumentar o tempo de espera, se necessário)
        time.sleep(5)
    except TimeoutException:
        print("Login form not found or login timed out.")


def scrape_followers(bot, username, user_input):
    bot.get(f'https://www.instagram.com/{username}/')
    time.sleep(3.5)
    WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()
    time.sleep(2)
    print(f"[Info] - Scraping followers for {username}...")

    users = set()

    while len(users) < user_input:
        followers = bot.find_elements(By.XPATH, "//a[contains(@href, '/')]")

        for i in followers:
            href = i.get_attribute('href')
            if href:
                #Adiciona o símbolo "@" antes do nome
                users.add('' + href.split("/")[3])  # Add "@" symbol before the name
            else:
                continue

        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(1)

    users = list(users)[:user_input]  # Trim the user list to match the desired number of followers

    print(f"[Info] - Saving followers for {username}...")
    with open(f'{username}_followers.txt', 'a') as file:
        file.write('\n'.join(users) + "\n")

def scrape_following(bot, username, user_input2):
    bot.get(f'https://www.instagram.com/{username}/')
    time.sleep(3.5)
    WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/following')]"))).click()
    time.sleep(2)
    print(f"[Info] - Scraping followings for {username}...")

    users = set()

    while len(users) < user_input2:
        followers = bot.find_elements(By.XPATH, "//a[contains(@href, '/')]")

        for i in followers:
            href = i.get_attribute('href')
            if href:
                #Adiciona o símbolo "@" antes do nome
                users.add('' + href.split("/")[3])  # Add "@" symbol before the name
            else:
                continue

        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(1)

    users = list(users)[:user_input2]  # Trim the user list to match the desired number of followers

    print(f"[Info] - Saving following for {username}...")
    with open(f'{username}_following.txt', 'a') as file:
        file.write('\n'.join(users) + "\n")


def scrape():
    user_input = int(input('[Required] - How many followers do you want to scrape (100-2000 recommended): '))
    user_input2 = int(input('[Required] - How many following do you want to scrape (100-2000 recommended): '))
    
    usernames = input("Enter the Instagram usernames you want to scrape (separated by commas): ").split(",")
    # Para windows
    os.environ["webdriver.chrome.driver"] = "chromedriver-win32\chromedriver-win32\chromedriver.exe"
    # Para MAC OSX
    #os.environ["webdriver.chrome.driver"] = "/usr/local/bin/chromedriver"  # Substitua pelo caminho correto do ChromeDriver no MAC
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")    # se remover o comentário, tudo irá acontecer em segundo plano
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(options=options)

    login_url = 'https://www.instagram.com/accounts/login/'
    username = 'celtacruel'
    password = 'Girafa:123'

    login(bot, login_url, username, password)

    for user in usernames:
        user = user.strip()
        scrape_followers(bot, user, user_input)
        scrape_following(bot, user, user_input)
    bot.quit()


def get_non_follow_back_users(username):

    username = scrape_following(username)
    try:
        with open(f'{username}_following.txt', 'r') as file:
            following = file.read().splitlines()
        with open(f'{username}_followers.txt', 'r') as file:
            followers = file.read().splitlines()
        not_following_back = [user for user in following if user not in followers]
        print(f"[Info] - Users who {username} is following but are not following back: {not_following_back}")
        with open(f'{username}_not_following_back.txt', 'a') as file:
            file.write('\n'.join(not_following_back) + "\n")
        return not_following_back
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []

if __name__ == '__main__':
    TIMEOUT = 15
    scrape()
    get_non_follow_back_users()
