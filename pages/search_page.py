from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from tests.general import Page, Component


class SearchPage(Page):
    PATH = '/search'

    @property
    def search(self):
        return Search(self.driver)

    def filter(self):
        return Filter(self.driver)

    @property
    def results(self):
        return SearchResults(self.driver)


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
    RESULTS = '//div[@class="search-results__items"]//section'

    ITEM = '//div[@class ="search-results__items"]//section[{}]'
    JOB_LINK = RESULTS + '//a[@href="/jobs/{}"]'
    JOB_TITLE = ITEM + '//a[@class="job-item__title"]'
    JOB_BUDGET = ITEM + '//span[@class="job-item__budget"]'
    JOB_SMALL_INFO = ITEM + '//div[contains(@class, "job-item__small__info")]'
    JOB_DESCRIPTION = ITEM + '//div[@class="job-item__description"]'
    JOB_TAGS = ITEM + '//div[@class="job-item__tags"]//span'
    JOB_COUNTRY = ITEM + '//span[@class="job-item__country"]'
    FL_NAME = ITEM + '//a[@class="freelancer-item__name"]'

    def get_jobs(self):
        results_raw = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_all_elements_located((By.XPATH, self.RESULTS))
        )

        results = []
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
        print("TEST FUCKING XPAAAATH: ", self.JOB_LINK.format(job_id))
        link = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOB_LINK.format(job_id)))
        )
        link.click()


class Filter(Component):


    def method(self):
        return
