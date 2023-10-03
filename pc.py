
def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--start-maximized', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    wait = WebDriverWait(
        driver,
        50,
        poll_frequency=5,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )

    return driver,wait



pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
