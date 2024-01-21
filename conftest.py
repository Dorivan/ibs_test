import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en',
                     help="Choose language: ru or en")


@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")

    browser = None

    if browser_name == "chrome":
        chrome_path = r"C:/chromedriver"
        options = Options()
        options.add_experimental_option(
            'prefs', {'intl.accept_languages': user_language}
        )
        print("\nstart browser Chrome for test..")
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options_firefox = FirefoxOptions()
        options_firefox.set_preference(
            "intl.accept_languages", user_language
        )
        print("\nstart browser FF for test..")
        browser = webdriver.Firefox(options=options_firefox)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield browser
    print("\nquit browser..")
    browser.quit()

@pytest.fixture(scope="session")
def session():
    session = requests.Session()
    yield session
    session.close()
