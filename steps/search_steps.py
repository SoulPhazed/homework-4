from tests.general import Step
from pages.search_page import SearchPage
from steps.job_for_search import JobStepsForSearch


class SearchSteps(Step):
    def query_search(self, query):
        page = SearchPage(self.driver)
        page.search.fill_input(query)
        page.search.submit()

        return

    def get_results(self):
        page = SearchPage(self.driver)
        return page.results.get_jobs()

    def switch_to_freelancers(self):
        page = SearchPage(self.driver)
        page.open()
        page.search.switch_to_freelancers()

    def switch_to_jobs(self):
        page = SearchPage(self.driver)
        page.open()
        page.search.switch_to_jobs()

    def go_to_job(self, job_id):
        page = SearchPage(self.driver)
        page.results.go_to_job(job_id)

    def compare_url_with_id(self, expected):
        job_steps = JobStepsForSearch(self.driver)
        if job_steps.get_job_id() != expected:
            return False
        else:
            return True
