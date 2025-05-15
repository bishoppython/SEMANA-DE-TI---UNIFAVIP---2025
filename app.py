# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time
# import csv

# # ---------------- CONFIGURAÇÃO ----------------
# search_term = input("Digite a vaga buscada: ")  # Substitua pela vaga desejada
# output_csv = "vagas_gupy.csv"
# # ------------------------------------------------

# # Inicializa o WebDriver com webdriver_manager
# options = webdriver.ChromeOptions()
# # options.add_argument('--headless')  # Descomente para rodar em modo headless

# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()),
#     options=options
# )

# try:
#     # 1) Abre a página da Gupy
#     driver.get("https://portal.gupy.io/")
#     time.sleep(3)  # Aguarda carregamento inicial
#     print("Entrando na página da Gupy...")
#     # Aguarda até que o botão de aceitar cookies esteja presente
#     try:
#         accept_cookies_button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
#         accept_cookies_button.click()
#         print("Cookies aceitos.")
#     except Exception as e:
#         print("Erro ao aceitar cookies:", e)
#     time.sleep(3)  # Aguarda carregamento após aceitar cookies
#     # Aguarda até que o botão de busca esteja presente
#     try:
#         search_button = driver.find_element(By.XPATH, '//*[@id="undefined-input"]')
#         search_button.click()
#         print("Botão de busca encontrado.")
#     except Exception as e:
#         print("Erro ao encontrar o botão de busca:", e)
#     time.sleep(3)  # Aguarda carregamento após clicar no botão de busca
#     # Aguarda até que o campo de busca esteja presente
#     try:
#         search_input = driver.find_element(By.XPATH, '//*[@id="undefined-input"]')
#         print("Campo de busca encontrado.")
#     except Exception as e:
#         print("Erro ao encontrar o campo de busca:", e)

#     # # 2) Localiza o campo de busca e digita a vaga
#     # search_input = driver.find_element(By.XPATH, '//*[@id="undefined-input"]')
#     # search_input.send_keys(search_term)
#     # search_input.send_keys(Keys.ENTER)

#     # 3) Espera 12 segundos pela listagem de vagas
#     time.sleep(12)

#     # 4) Prepara o arquivo CSV
#     with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.writer(file)
#         writer.writerow(["Título da Vaga", "Link"])  # Cabeçalho

#         prev_count = 0
#         while True:
#             # Coleta todas as vagas carregadas até o momento
#             cards = driver.find_elements(By.CSS_SELECTOR, ".sc-4d881605-0.kokxPe")
#             total = len(cards)

#             # Se não houver novas vagas, interrompe o loop
#             if total <= prev_count:
#                 break

#             # Itera apenas sobre as novas vagas
#             for card in cards[prev_count:]:
#                 try:
#                     # Extrai link e título
#                     link_el = card.find_element(By.TAG_NAME, "a")
#                     link = link_el.get_attribute("href")
#                     title = link_el.text.strip()
#                     writer.writerow([title, link])
#                 except Exception:
#                     continue

#             prev_count = total

#             # 5) Rola a página até o fim e aguarda 6 segundos
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(6)

#     # 6) Aguarda 13 segundos antes de fechar
#     time.sleep(13)

# finally:
#     driver.quit()

# print(f"Dados de {prev_count} vagas salvos em '{output_csv}'")

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

search_term = "python"
output_csv = "vagas_gupy.csv"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://portal.gupy.io/")
    time.sleep(3)

    # aceita cookies se presente
    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        time.sleep(1)
    except:
        pass

    # busca
    inp = driver.find_element(By.XPATH, '//*[@id="undefined-input"]')
    inp.send_keys(search_term + "\n")
    time.sleep(10)  # aguarda resultados

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Empresa", "Título da Vaga", "Tipo de Trabalho", "Link", "Data"])

        prev = 0
        while True:
            cards = driver.find_elements(By.XPATH, '//*[@id="main-content"]/ul/li')
            if len(cards) <= prev:
                break

            for card in cards[prev:]:
                try:
                    # link e título
                    a = card.find_element(By.TAG_NAME, "a")
                    link = a.get_attribute("href")
                    title = card.find_element(By.TAG_NAME, "h3").text.strip()

                    # empresa (ajuste o seletor conforme o DOM real)
                    try:
                        company = card.find_element(By.CSS_SELECTOR, "p[class*='company']").text.strip()
                    except:
                        company = ""

                    # tipo de trabalho
                    try:
                        work_type = card.find_element(
                            By.XPATH,
                            ".//span[contains(text(),'Remoto') or contains(text(),'Presencial') or contains(text(),'Híbrido')]"
                        ).text.strip()
                    except:
                        work_type = ""

                    # data (procura a tag <time> interna)
                    try:
                        date = card.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                    except:
                        date = ""

                    writer.writerow([company, title, work_type, link, date])
                except:
                    continue

            prev = len(cards)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

finally:
    driver.quit()
    print(f"Salvas {prev} vagas em {output_csv}")
