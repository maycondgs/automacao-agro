from selenium import webdriver

# Configuração do driver (geckodriver)
geckodriver_path = '/usr/bin/geckodriver'
driver = webdriver.Firefox(executable_path=geckodriver_path)

# Exemplo: abrindo o Google
driver.get('https://www.google.com')

# Encerrando o driver
driver.quit()