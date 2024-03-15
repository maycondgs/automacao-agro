from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os

# Configuração do driver (geckodriver)
geckodriver_path = '/usr/bin/geckodriver'
os.environ['PATH'] += os.pathsep + geckodriver_path

firefox_options = Options()
firefox_options.headless = True

driver = webdriver.Firefox()

# Exemplo: abrindo o Google
driver.get('https://www.google.com')

# Encerrando o driver
driver.quit()