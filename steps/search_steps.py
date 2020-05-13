from tests.general import Step
from pages.search_page import SearchPage
from steps.job_for_search import JobStepsForSearch
from steps.profile_for_search import ProfileStepsForSearch


class SearchSteps(Step):
    def query_search(self, query):
        page = SearchPage(self.driver)
        page.search.fill_input(query)
        page.search.submit()

        return

    def get_results(self, limit=None):
        page = SearchPage(self.driver)
        if page.search.get_search_type() == "jobs":
            return page.results.get_jobs(limit)
        else:
            return page.results.get_freelancers(limit)

    def open_freelancers(self):
        page = SearchPage(self.driver)
        page.open()
        page.search.switch_to_freelancers()

    def open_jobs(self):
        page = SearchPage(self.driver)
        page.open()
        page.search.switch_to_jobs()

    def go_to_job(self, job_id):
        page = SearchPage(self.driver)
        page.results.go_to_job(job_id)

    def compare_job_url_with_id(self, expected):
        job_steps = JobStepsForSearch(self.driver)
        if job_steps.get_job_id() != expected:
            return False
        else:
            return True

    def compare_fl_url_with_id(self, expected):
        profile_steps = ProfileStepsForSearch(self.driver)
        if profile_steps.get_profile_id() != expected:
            return False
        else:
            return True

    def set_job_type(self, job_type):
        page = SearchPage(self.driver)
        page.filter.set_job_type(job_type)

    def set_budget(self, from_value=None, to_value=None):
        page = SearchPage(self.driver)
        if to_value:
            page.filter.set_budget_to(to_value)
        if from_value:
            page.filter.set_budget_from(from_value)

    def increment_budget(self, field, increment):
        page = SearchPage(self.driver)
        if field == "from":
            page.filter.increment_budget_from(increment)
        elif field == "to":
            page.filter.increment_budget_to(increment)
        else:
            raise AttributeError("'field' attr must be 'from' or 'to'")

    def get_budget_from_error(self):
        page = SearchPage(self.driver)
        return page.filter.get_budget_from_error()

    def set_category(self, category):
        page = SearchPage(self.driver)
        page.filter.set_category(category)

    def set_speciality(self, speciality):
        page = SearchPage(self.driver)
        page.filter.set_speciality(speciality)

    def set_level(self, level):
        page = SearchPage(self.driver)
        page.filter.set_level(level)

    def set_country(self, country):
        page = SearchPage(self.driver)
        page.filter.set_country(country)

    def set_city(self, city):
        page = SearchPage(self.driver)
        page.filter.set_city(city)

    def set_proposals(self, condition):
        if condition not in ["more", "less"]:
            raise AttributeError("'condition' attr must be 'more' or 'less'")

        page = SearchPage(self.driver)
        page.filter.set_proposals(condition)

    def go_to_freelancer(self, fl_id):
        page = SearchPage(self.driver)
        page.results.go_to_freelancer(fl_id)
