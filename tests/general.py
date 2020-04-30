from urllib.parse import urljoin

# WebDriverWait - ожидание браузера события
# expected_conditions - состояния элемента, которые работают вместе с ожиданием
# By - используется совместно с expected_conditions - указание, по чему искать элемент (тип селектора)


class Page(object):
    BASE_URL = 'http://fwork.live/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class Step(object):
    def __init__(self, driver):
        self.driver = driver
