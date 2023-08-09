def iniciar_driver():
    chrome_options = Options()

    arguments = ['--window-size=1000,800',
                 '--incognito', '--disable-gpu', '--no-sandbox', '--headless', '--disable-dev-shm-usage']

    for argument in arguments:
        chrome_options.add_argument(argument)
    chrome_options.headless = True
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager(version="114.0.5735.90").install()), options=chrome_options)

    return driver



pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
