import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote
from steps.job_for_search import JobStepsForSearch
from steps.auth_steps import AuthSteps
from steps.search_steps import SearchSteps


class SearchTest(unittest.TestCase):
    TYPE = None

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        self.JOB_DATA = {
            "id": "-1",
            "title": "Default Title from Selenium",
            "tags": ["Python", "Selenium"],
            "description": "Test work from selenium",
            "category": "Программирование",
            "speciality": "QA (тестирование)",
            "type": "Проект",
            "budget": "10000",
            "level": "Продвинутый",
            "country": "Россия",
            "city": "Москва",
        }

        auth_steps = AuthSteps(self.driver)
        auth_steps.login_as_client()

        job_steps = JobStepsForSearch(self.driver)
        job_steps.create_custom(self.JOB_DATA)

        self.JOB_DATA["id"] = job_steps.get_job_id()

    def tearDown(self):
        my_jobs = JobStepsForSearch(self.driver)
        my_jobs.delete_job(self.JOB_DATA["id"])

        self.driver.quit()


def find_job_in_results(array, job):
    for item in array:
        if (item["title"] == job["title"]) and (item["description"] == job["description"]) and (
                item["tags"] == job["tags"]) and (item["country"] == job["country"]):
            return True
    return False


class SearchCrossToJobPageTest(SearchTest):
    def test(self):
        search_steps = SearchSteps(self.driver)
        search_steps.switch_to_jobs()
        search_steps.query_search(self.JOB_DATA["title"])
        search_steps.go_to_job(self.JOB_DATA["id"])
        self.assertTrue(search_steps.compare_url_with_id(expected=self.JOB_DATA["id"]))


class SearchFindJobByTagTest(SearchTest):
    def test(self):
        search_steps = SearchSteps(self.driver)
        search_steps.switch_to_jobs()
        search_steps.query_search(self.JOB_DATA["tags"][0])
        results = search_steps.get_results()
        self.assertTrue(find_job_in_results(array=results, job=self.JOB_DATA))


class SearchFindJobByTitleTest(SearchTest):
    def test(self):
        search_steps = SearchSteps(self.driver)
        search_steps.switch_to_jobs()
        search_steps.query_search(self.JOB_DATA["title"])
        results = search_steps.get_results()
        self.assertTrue(find_job_in_results(array=results, job=self.JOB_DATA))

