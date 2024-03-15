from selenium import webdriver
import os

# Configuração do driver (geckodriver)
geckodriver_path = '/usr/bin/geckodriver'
os.environ['PATH'] += os.pathsep + geckodriver_path

driver = webdriver.Firefox()

# Exemplo: abrindo o Google
driver.get('https://www.google.com')

# Encerrando o driver
driver.quit()