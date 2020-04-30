import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

from tests.general import Page, Component


class CreateJobPageForSearch(Page):
    PATH = '/new-job'
    CREATE_BTN = '//a[contains(@href,"/new-job")]'

    @property
    def form(self):
        return JobFormForSearch(self.driver)

    def open_form(self):
        new_job_button = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.CREATE_BTN))
        )
        new_job_button.click()

    @property
    def new_job(self):
        return NewJob(self.driver)


class MyJobsPageForSearch(Page):
    PATH = '/my-job-postings'

    @property
    def jobs(self):
        return ManageJobs(self.driver)


class JobFormForSearch(Component):
    JOB_TYPE = '//input[@name="jobTypeId" and @value="{}"]'
    JOB_LEVEL = '//input[@name="experienceLevelId" and @value="{}"]'
    JOB_TITLE = '//input[@name="title"]'
    JOB_DESCRIPTION = '//textarea[@name="description"]'
    JOB_BUDGET = '//input[@name="paymentAmount"]'
    JOB_TAGS = '//input[contains(@class, "input-tags__input")]'
    JOB_COUNTRY_SELECT = '//div[./select[@name="country"]]/div/div'
    JOB_COUNTRY_ITEM = JOB_COUNTRY_SELECT + '//li[@data-val="{}"]'
    JOB_CITY_SELECT = '//div[./select[@name="city"]]/div/div'
    JOB_CITY_ITEM = JOB_CITY_SELECT + '//li[@data-val="{}"]'
    JOB_SPECIALITY_SELECT = '//div[./select[@name="specialityId"]]/div/div'
    JOB_SPECIALITY_ITEM = JOB_SPECIALITY_SELECT + '//li[@data-val="{}"]'
    JOB_CATEGORY_SELECT = '//div[./label/text()="Категория"]/div/div'
    JOB_CATEGORY_ITEM = JOB_CATEGORY_SELECT + '//li[@data-val="{}"]'
    SUBMIT = '//form[@id="projectForm"]//button[@type="submit"]'

    JOB_TYPE_MATCH = {
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
        "Начинающий": "1",
        "Продвинутый": "2",
        "Эксперт": "3",
    }

    def set_type(self, job_type):
        job_type_inner = self.JOB_TYPE_MATCH[job_type]
        if not job_type_inner:
            job_type_inner = 0

        type_radio = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, self.JOB_TYPE.format(job_type_inner)))
        )
        type_radio.click()

    def set_title(self, title):
        title_input = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_TITLE))
        )
        title_input.clear()
        title_input.send_keys(title)
        self.driver.find_element(By.XPATH, "//h1").click()

    def set_description(self, description):
        descr_input = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_DESCRIPTION))
        )
        descr_input.clear()
        descr_input.send_keys(description)
        self.driver.find_element(By.XPATH, "//h1").click()

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
        time.sleep(0.5)

    def set_spec(self, speciality):
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

    def set_tags(self, tags):
        tags_input = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_TAGS))
        )
        tags_input.clear()
        for tag in tags:
            tags_input.send_keys(tag)
            tags_input.send_keys('\uE007')

    def set_budget(self, budget):
        budget_input = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_BUDGET))
        )
        budget_input.clear()
        budget_input.send_keys(budget)

    def set_country(self, country):
        country_inner = self.COUNTRY_MATCH[country]
        if not country_inner:
            country_inner = 0

        country_select = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_COUNTRY_SELECT))
        )
        country_select.click()
        country_item = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_COUNTRY_ITEM.format(country_inner)))
        )
        country_item.click()
        time.sleep(0.5)

    def set_city(self, city):
        city_inner = self.CITY_MATCH[city]
        if not city_inner:
            city_inner = 0

        city_select = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_CITY_SELECT))
        )
        city_select.click()
        city_item = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_CITY_ITEM.format(city_inner)))
        )
        city_item.click()
        time.sleep(0.5)

    def set_level(self, level):
        level_inner = self.LEVELS_MATCH[level]
        if not level_inner:
            level_inner = 1

        type_radio = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, self.JOB_LEVEL.format(level_inner)))
        )
        type_radio.click()

    def submit(self):
        submit = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.SUBMIT))
        )
        submit.click()


class NewJob(Component):
    def get_id(self):
        WebDriverWait(self.driver, 10).until(
            ec.url_contains("jobs")
        )
        return self.driver.current_url.split('/')[-1]


class ManageJobs(Component):
    JOB_ITEM = '//div[./a[@href="/jobs/{}"]]'
    DELETE = JOB_ITEM + '//button[contains(@class, "delete-job-action")]'
    DELETE_CONFIRMATION = '//div[contains(@class, "modal-window")]//button[@type="submit"]'

    def delete_job(self, job_id):
        job_item = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, self.JOB_ITEM.format(job_id)))
        )
        action = ActionChains(self.driver)
        action.move_to_element(job_item).perform()
        delete = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.DELETE.format(job_id)))
        )
        delete.click()

    def confirm_delete(self):
        delete = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.DELETE_CONFIRMATION))
        )
        delete.click()
        time.sleep(1)
