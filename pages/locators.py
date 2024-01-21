from selenium.webdriver.common.by import By

class BasePageLocators:
    REQUEST_URL = (By.XPATH, "//span[@class='url']")
    REQUEST_BODY = (By.XPATH, "//pre[@data-key='output-request']")

    RESPONSE_CODE = (By.XPATH, "//span[contains(@class,'response-code')]")
    RESPONSE_BODY = (By.XPATH, "//pre[@data-key='output-response']")

    ENDPOINT_LIST = (By.CSS_SELECTOR, ".endpoints")
    ENDPOINT_ELEMENT = (By.XPATH, "//div[@class='endpoints']/ul/li")

    SPINNER = (By.XPATH, "//div[@class='spinner']")
    