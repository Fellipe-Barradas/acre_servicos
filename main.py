from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pandas import DataFrame
import time

def get_last_page_num(driver: webdriver.Chrome) -> int:
    driver.implicitly_wait(5)
    total_paginas = driver.find_elements(By.XPATH,'//a[@class="btn btn-outline-primary"]')
    ultima_pagina = int(total_paginas[-2].text)
    return ultima_pagina

def get_card_data(driver: webdriver.Chrome) -> dict:
    time.sleep(3)
    cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'cartoes_modalidade')]")
    card_data = []
    for card in cards:
        titulo = card.find_element(By.XPATH, ".//h5").text
        descricao = card.find_element(By.XPATH, ".//p").text
        footer = card.find_elements(By.XPATH, ".//div[contains(@class, 'card-footer')]")
        orgao = footer[0].get_attribute("data-bs-title")
        card_data.append({"titulo": titulo, "descricao": descricao, "orgao": orgao})
    return card_data

def main():
    pagina = 1
    url = f"https://www.ac.gov.br/categorias/administracao-publica?pagina={pagina}"
    
    # Criar uma instância do Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    # Acessar a url
    driver.get(url)
    
    # Coletar os dados da página inicial
    card_data = get_card_data(driver)
    
    # Buscar a ultima página da paginação
    ultima_pagina = get_last_page_num(driver)
    
    # Carregar os dados das demais páginas
    for pagina in range(2, ultima_pagina+1):
        driver.execute_script(f"javascript:carregarServicos('https://www.ac.gov.br/categorias/administracao-publica?pagina={pagina}')")
        card_data += get_card_data(driver)

    # Fechar o navegador
    driver.quit()
    
    # Salvar os dados em um arquivo CSV
    card_data = DataFrame(card_data)
    card_data.to_csv("cards.csv", index=False)
    
if __name__ == "__main__":
    main()