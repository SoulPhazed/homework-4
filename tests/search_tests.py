import os
import unittest
from copy import deepcopy

from selenium.webdriver import DesiredCapabilities, Remote
from steps.job_for_search import JobStepsForSearch
from steps.auth_steps import AuthSteps
from steps.search_steps import SearchSteps
from steps.profile_for_search import ProfileStepsForSearch


def find_job_in_results(array, job):
    for item in array:
        if (item["title"] == job["title"]) and (item["description"] == job["description"]) and (
                item["tags"] == job["tags"]) and (item["country"] == job["country"]):
            return True
    return False


def find_freelancer_in_results(array, freelancer):
    for item in array:
        if (item["first_name"] == freelancer["first_name"]) and (item["last_name"] == freelancer["last_name"]) and (
                item["speciality"] == freelancer["speciality"]) and (item["country"] == freelancer["country"]):
            return True
    return False


def find_position_among_results(array, item_id):
    for i in range(len(array)):
        if find_job_in_results([array[i]], array[i]):
            if array[i]["id"] == item_id:
                return i
    return None


class SearchJobsTest(unittest.TestCase):
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
        search_steps = SearchSteps(self.driver)

        auth_steps.login_as_client()
        job_steps = JobStepsForSearch(self.driver)
        job_steps.create_custom(self.JOB_DATA)

        self.JOB_DATA["id"] = job_steps.get_job_id()
        search_steps.open_jobs()

    def tearDown(self):
        my_jobs = JobStepsForSearch(self.driver)
        my_jobs.delete_job(self.JOB_DATA["id"])

        self.driver.quit()

    def test_cross_to_page(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["title"])
        search_steps.go_to_job(self.JOB_DATA["id"])
        self.assertTrue(search_steps.compare_job_url_with_id(expected=self.JOB_DATA["id"]))

    def test_sorting(self):
        job_data_second = deepcopy(self.JOB_DATA)
        job_steps = JobStepsForSearch(self.driver)
        job_steps.create_custom(job_data_second)
        job_data_second["id"] = job_steps.get_job_id()

        search_steps = SearchSteps(self.driver)
        search_steps.open_jobs()
        search_steps.query_search(self.JOB_DATA["title"])
        results = search_steps.get_results()
        first_id = find_position_among_results(array=results, item_id=self.JOB_DATA["id"])
        second_id = find_position_among_results(array=results, item_id=job_data_second["id"])

        job_steps.delete_job(job_data_second["id"])

        self.assertTrue(second_id < first_id)

    def test_find_by_tag(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["tags"][0])
        results = search_steps.get_results()

        self.assertTrue(find_job_in_results(array=results, job=self.JOB_DATA))

    def test_find_by_title(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["title"])
        results = search_steps.get_results()

        self.assertTrue(find_job_in_results(array=results, job=self.JOB_DATA))

    def test_filter_by_type(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["title"])
        search_steps.set_job_type(self.JOB_DATA["type"])
        results = search_steps.get_results()

        self.assertTrue(find_job_in_results(array=results, job=self.JOB_DATA))

    def test_filter_by_speciality(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["title"])
        search_steps.set_category(self.JOB_DATA["category"])
        search_steps.set_speciality(self.JOB_DATA["speciality"])
        results = search_steps.get_results()

        self.assertTrue(find_job_in_results(array=results, job=self.JOB_DATA))

    def test_filter_by_budget(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["title"])
        search_steps.set_budget(from_value=int(self.JOB_DATA['budget']) - 100,
                                to_value=int(self.JOB_DATA['budget']) + 100)
        results = search_steps.get_results()

        self.assertTrue(find_job_in_results(array=results, job=self.JOB_DATA))

    def test_filter_increment_budget(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["title"])
        search_steps.set_budget(from_value=int(self.JOB_DATA['budget']) + 5,
                                to_value=int(self.JOB_DATA['budget']) + 100)
        result_before = find_job_in_results(array=search_steps.get_results(), job=self.JOB_DATA)
        search_steps.increment_budget(field="from", increment=-5)
        result_after = find_job_in_results(array=search_steps.get_results(), job=self.JOB_DATA)

        self.assertTrue(not result_before and result_after)

    def test_filter_budget_from_error(self):
        search_steps = SearchSteps(self.driver)
        search_steps.set_budget(from_value=100, to_value=10)
        error_msg = search_steps.get_budget_from_error()

        self.assertTrue(error_msg)

    def test_filter_by_country(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["title"])
        search_steps.set_country(self.JOB_DATA["country"])
        results = search_steps.get_results()

        self.assertTrue(find_job_in_results(array=results, job=self.JOB_DATA))

    def test_filter_by_city(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["title"])
        search_steps.set_country(self.JOB_DATA["country"])
        search_steps.set_city(self.JOB_DATA["city"])
        results = search_steps.get_results()

        self.assertTrue(find_job_in_results(array=results, job=self.JOB_DATA))

    def test_filter_by_proposals(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.JOB_DATA["title"])
        search_steps.set_proposals("more")
        results = search_steps.get_results()

        self.assertTrue(not find_job_in_results(array=results, job=self.JOB_DATA))


class SearchFreelancersTest(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        auth_steps = AuthSteps(self.driver)
        profile_steps = ProfileStepsForSearch(self.driver)
        search_steps = SearchSteps(self.driver)

        auth_steps.login_as_freelancer()
        self.FREELANCER_DATA = profile_steps.get_info()
        search_steps.open_freelancers()

    def tearDown(self):
        self.driver.quit()

    def test_cross_to_page(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.FREELANCER_DATA["last_name"])
        search_steps.go_to_freelancer(self.FREELANCER_DATA["id"])
        self.assertTrue(search_steps.compare_fl_url_with_id(expected=self.FREELANCER_DATA["id"]))

    def test_sorting(self):
        search_steps = SearchSteps(self.driver)
        freelancers = search_steps.get_results(limit=2)

        self.assertTrue(freelancers[0]["id"] > freelancers[1]["id"])

    def test_find_by_skills(self):
        DEFAULT_SKILLS = ['Selenium']
        DEFAULT_DESCRIPTION = "Description from Selenium"
        profile_steps = ProfileStepsForSearch(self.driver)
        search_steps = SearchSteps(self.driver)

        if len(self.FREELANCER_DATA['skills']) == 0:
            profile_steps.open_settings_form()
            profile_steps.set_skills(DEFAULT_SKILLS)
            self.FREELANCER_DATA['skills'] = DEFAULT_SKILLS

            if not self.FREELANCER_DATA['description']:
                profile_steps.set_description(DEFAULT_DESCRIPTION)
                self.FREELANCER_DATA['description'] = DEFAULT_DESCRIPTION
            profile_steps.submit_settings()

        search_steps.open_freelancers()
        search_steps.query_search(self.FREELANCER_DATA["skills"][0])
        freelancers = search_steps.get_results()

        self.assertTrue(find_freelancer_in_results(array=freelancers, freelancer=self.FREELANCER_DATA))

    def test_find_by_name(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.FREELANCER_DATA["first_name"] + " " + self.FREELANCER_DATA["last_name"])
        freelancers = search_steps.get_results()

        self.assertTrue(find_freelancer_in_results(array=freelancers, freelancer=self.FREELANCER_DATA))

    def test_filter_by_level(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.FREELANCER_DATA["last_name"])
        search_steps.set_level(self.FREELANCER_DATA["level"])
        freelancers = search_steps.get_results()

        self.assertTrue(find_freelancer_in_results(array=freelancers, freelancer=self.FREELANCER_DATA))

    def test_filter_by_city(self):
        search_steps = SearchSteps(self.driver)
        search_steps.query_search(self.FREELANCER_DATA["last_name"])
        search_steps.set_country(self.FREELANCER_DATA['country'])
        search_steps.set_city(self.FREELANCER_DATA["city"])
        freelancers = search_steps.get_results()

        self.assertTrue(find_freelancer_in_results(array=freelancers, freelancer=self.FREELANCER_DATA))
