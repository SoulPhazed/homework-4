import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from tests.general import Page, Component
from pages.menu_component import ProfileMenu


def wait_results_required(func):
    def func_wrapper(self, *args, **kwargs):
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, self.IS_RESULTS))
        )
        func(self, *args, **kwargs)
    return func_wrapper


class SearchPage(Page):
    PATH = '/search'

    @property
    def search(self):
        return Search(self.driver)

    @property
    def filter(self):
        return Filter(self.driver)

    @property
    def results(self):
        return SearchResults(self.driver)

    @property
    def user_menu(self):
        return ProfileMenu(self.driver)


class Search(Component):
    INPUT = '//div[@class="search-input__input"]//input[@type="search"]'
    SUBMIT = '//div[@class="search-input__submit"]//button[@type="submit"]'
    JOBS_SWITCH = '//ul[contains(@class, "tabs__nav")]//a[contains(@href, "jobs")]'
    FREELANCERS_SWITCH = '//ul[contains(@class, "tabs__nav")]//a[contains(@href, "freelancers")]'

    def switch_to_jobs(self):
        switcher = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOBS_SWITCH))
        )
        switcher.click()

    def switch_to_freelancers(self):
        switcher = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.FREELANCERS_SWITCH))
        )
        switcher.click()

    def fill_input(self, query):
        search_input = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.INPUT))
        )
        search_input.clear()
        search_input.send_keys(query)

    def submit(self):
        search_submit = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.SUBMIT))
        )
        search_submit.click()


class SearchResults(Component):
    IS_RESULTS = '//div[div[@class="search-results__items"]/section or div[@class="search-not-found"]//img]'
    RESULTS = '//div[@class="search-results__items"]//section'
    NOT_FOUND = '//div[@class="search-not-found"]//img'
    ITEM = '//div[@class ="search-results__items"]//section[{}]'

    JOB_LINK = RESULTS + '//a[@href="/jobs/{}"]'
    JOB_TITLE = ITEM + '//a[@class="job-item__title"]'
    JOB_BUDGET = ITEM + '//span[@class="job-item__budget"]'
    JOB_SMALL_INFO = ITEM + '//div[contains(@class, "job-item__small__info")]'
    JOB_DESCRIPTION = ITEM + '//div[@class="job-item__description"]'
    JOB_TAGS = ITEM + '//div[@class="job-item__tags"]//span'
    JOB_COUNTRY = ITEM + '//span[@class="job-item__country"]'

    FL_LINK = RESULTS + '//a[@href="/freelancers/{}"]'
    FL_NAME = ITEM + '//a[@class="freelancer-item__name"]'
    FL_SPECIALITY = ITEM + '//div[a[@class = "freelancer-item__name"]]/*[contains(text(), "Специализация")]'
    FL_COUNTRY = ITEM + '//li[@class="freelancer-item__block-info-item"]'

    def get_jobs(self):
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, self.IS_RESULTS))
        )

        try:
            not_found = self.driver.find_element(By.XPATH, self.NOT_FOUND)
        except NoSuchElementException:
            not_found = False

        results = []
        if not not_found:
            results_raw = WebDriverWait(self.driver, 15).until(
                ec.visibility_of_all_elements_located((By.XPATH, self.RESULTS))
            )
            for i in range(1, len(results_raw) + 1):
                type_level_date = self.driver.find_element(By.XPATH, self.JOB_SMALL_INFO.format(i)).text.split(" - ")

                job_data = {
                    "id": self.driver.find_element(By.XPATH, self.JOB_TITLE.format(i)).get_attribute("href").split('/')[-1],
                    "title": self.driver.find_element(By.XPATH, self.JOB_TITLE.format(i)).text,
                    "tags": [tag.text for tag in self.driver.find_elements(By.XPATH, self.JOB_TAGS.format(i))],
                    "description": self.driver.find_element(By.XPATH, self.JOB_DESCRIPTION.format(i)).text,
                    "type": type_level_date[0].split(" ")[0],
                    "budget": self.driver.find_element(By.XPATH, self.JOB_BUDGET.format(i)).text.split(" ")[0],
                    "date": type_level_date[2],
                    "level": type_level_date[1],
                    "country": self.driver.find_element(By.XPATH, self.JOB_COUNTRY.format(i)).text
                }
                results.append(job_data)

        return results

    def go_to_job(self, job_id):
        link = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_LINK.format(job_id)))
        )
        link.click()

    def get_freelancers(self):
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, self.IS_RESULTS))
        )

        try:
            not_found = self.driver.find_element(By.XPATH, self.NOT_FOUND)
        except NoSuchElementException:
            not_found = False

        results = []
        if not not_found:
            results_raw = WebDriverWait(self.driver, 15).until(
                ec.visibility_of_all_elements_located((By.XPATH, self.RESULTS))
            )
            for i in range(1, len(results_raw) + 1):
                fl_name = self.driver.find_element(By.XPATH, self.FL_NAME.format(i)).text.split(" ")

                freelancer_data = {
                    "id": self.driver.find_element(By.XPATH, self.FL_NAME.format(i)).get_attribute("href").split('/')[
                        -1],
                    "first_name": fl_name[0],
                    "last_name": fl_name[1],
                    "speciality": self.driver.find_element(By.XPATH, self.FL_SPECIALITY.format(i)).text.split(" ")[-1],
                    "country": self.driver.find_element(By.XPATH, self.FL_COUNTRY.format(i)).text
                }
                results.append(freelancer_data)

        return results

    def go_to_freelancer(self, fl_id):
        link = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.FL_LINK.format(fl_id)))
        )

        link.click()


class Filter(Component):
    IS_RESULTS = '//div[div[@class="search-results__items"]/section or div[@class="search-not-found"]//img]'

    JOB_TYPE = '//input[@name="jobTypeId" and @value="{}"]'
    LEVEL = '//input[@name="experienceLevel" and @value="{}"]'
    JOB_BUDGET_FROM = '//input[@name="minPaymentAmount"]'
    JOB_BUDGET_FROM_ERROR = '//div[{}]/span[@class="text-field__error"]'.format(JOB_BUDGET_FROM)
    JOB_BUDGET_TO = '//input[@name="maxPaymentAmount"]'
    JOB_PROPOSALS_CHECK = '//label[input[@name="proposalCount" and @value="{}"]]/span[@class="checkmark"]'
    COUNTRY_SELECT = '//div[./select[@name="country"]]/div/div'
    COUNTRY_ITEM = COUNTRY_SELECT + '//li[@data-val="{}"]'
    CITY_SELECT = '//div[./select[@name="city"]]/div/div'
    CITY_ITEM = CITY_SELECT + '//li[@data-val="{}"]'
    JOB_SPECIALITY_SELECT = '//div[./select[@name="specialityId"]]/div/div'
    JOB_SPECIALITY_ITEM = JOB_SPECIALITY_SELECT + '//li[@data-val="{}"]'
    JOB_CATEGORY_SELECT = '//div[./label/text()="Категория"]/div/div'
    JOB_CATEGORY_ITEM = JOB_CATEGORY_SELECT + '//li[@data-val="{}"]'

    JOB_TYPE_MATCH = {
        "Все": "-1",
        "Проект": "0",
        "Вакансия": "1"
    }

    CATEGORY_MATCH = {
        "Программирование": "1"
    }

    SPECIALITY_MATCH = {
        "QA (тестирование)": "9"
    }

    COUNTRY_MATCH = {
        "Россия": "0"
    }

    CITY_MATCH = {
        "Москва": "1"
    }

    LEVELS_MATCH = {
        "Все": "111",
        "Начинающий": "100",
        "Продвинутый": "010",
        "Эксперт": "001",
    }

    PROPOSALS_MATCH = {
        "less": "0-10",
        "more": "10-1000",
    }

    @wait_results_required
    def set_job_type(self, job_type):
        job_type_inner = self.JOB_TYPE_MATCH[job_type]
        if not job_type_inner:
            job_type_inner = 0

        type_radio = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, self.JOB_TYPE.format(job_type_inner)))
        )
        type_radio.click()

    @wait_results_required
    def set_category(self, category):
        category_inner = self.CATEGORY_MATCH[category]
        if not category_inner:
            category_inner = 0

        category_select = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_CATEGORY_SELECT))
        )
        category_select.click()
        category_item = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_CATEGORY_ITEM.format(category_inner)))
        )
        category_item.click()
        time.sleep(1)

    @wait_results_required
    def set_speciality(self, speciality):
        speciality_inner = self.SPECIALITY_MATCH[speciality]
        if not speciality_inner:
            speciality_inner = 0

        speciality_select = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_SPECIALITY_SELECT))
        )
        speciality_select.click()
        speciality_item = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_SPECIALITY_ITEM.format(speciality_inner)))
        )
        speciality_item.click()
        time.sleep(0.5)

    @wait_results_required
    def set_country(self, country):
        country_inner = self.COUNTRY_MATCH[country]
        if not country_inner:
            country_inner = 0

        country_select = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.COUNTRY_SELECT))
        )
        country_select.click()
        country_item = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.COUNTRY_ITEM.format(country_inner)))
        )
        country_item.click()
        time.sleep(1)

    @wait_results_required
    def set_city(self, city):
        city_inner = self.CITY_MATCH[city]
        if not city_inner:
            city_inner = 0

        city_select = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.CITY_SELECT))
        )
        city_select.click()
        city_item = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.CITY_ITEM.format(city_inner)))
        )
        city_item.click()
        time.sleep(0.5)

    @wait_results_required
    def set_level(self, level):
        level_inner = self.LEVELS_MATCH[level]
        if not level_inner:
            level_inner = 1

        type_radio = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, self.LEVEL.format(level_inner)))
        )
        type_radio.click()

    @wait_results_required
    def set_budget_from(self, from_value):
        from_field = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_BUDGET_FROM))
        )
        from_field.clear()
        from_field.send_keys(from_value)
        # avoiding freezing bug
        self.driver.find_element(By.XPATH, "//h2").click()
        time.sleep(0.5)

    @wait_results_required
    def set_budget_to(self, to_value):
        to_field = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_BUDGET_TO))
        )
        to_field.clear()
        to_field.send_keys(to_value)
        # avoiding freezing bug
        self.driver.find_element(By.XPATH, "//h2").click()
        time.sleep(0.5)

    @wait_results_required
    def increment_budget_from(self, increment):
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_BUDGET_FROM))
        )

        if increment > 0:
            key = Keys.ARROW_UP
        else:
            key = Keys.ARROW_DOWN

        for i in range(abs(increment)):
            # avoiding losing of DOM reference bug
            from_field = self.driver.find_element(By.XPATH, self.JOB_BUDGET_FROM)
            from_field.send_keys(key)

    @wait_results_required
    def increment_budget_to(self, increment):
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_BUDGET_TO))
        )

        if increment > 0:
            key = Keys.ARROW_UP
        else:
            key = Keys.ARROW_DOWN

        for i in range(abs(increment)):
            # avoiding losing of DOM reference bug
            to_field = self.driver.find_element(By.XPATH, self.JOB_BUDGET_TO)
            to_field.send_keys(key)

    def get_budget_from_error(self):
        try:
            error_span = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, self.JOB_BUDGET_FROM_ERROR))
            )
        except TimeoutException:
            error_span = None

        if error_span:
            return error_span.text

        return None

    @wait_results_required
    def set_proposals(self, condition):
        proposals_check = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_PROPOSALS_CHECK.format(self.PROPOSALS_MATCH[condition])))
        )
        proposals_check.click()
