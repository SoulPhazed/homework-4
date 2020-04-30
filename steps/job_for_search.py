from tests.general import Step
from pages.job_for_search import CreateJobPageForSearch, MyJobsPageForSearch


class JobStepsForSearch(Step):
    def create_custom(self, data=None):
        data_inner = data
        if data is None:
            data_inner = {
                "title": "Default Title from Selenium",
                "tags": ["Python", "Selenium"],
                "description": "Test work from selenium",
                "category": "Программирование",
                "speciality": "QA (тестирование)",
                "type": "Проект",
                "budget": "10000",
                "level": "Начинающий",
                "country": "Россия",
                "city": "Москва",
            }

        page = CreateJobPageForSearch(self.driver)
        page.open_form()

        form = page.form
        form.set_type(data_inner["type"])
        form.set_title(data_inner["title"])
        form.set_description(data_inner["description"])
        form.set_category(data_inner["category"])
        form.set_spec(data_inner["speciality"])
        form.set_tags(data_inner["tags"])
        form.set_budget(data_inner["budget"])
        form.set_level(data_inner["level"])
        form.set_country(data_inner["country"])
        form.set_city(data_inner["city"])

        form.submit()

    def get_job_id(self):
        page = CreateJobPageForSearch(self.driver)
        return page.new_job.get_id()

    def delete_job(self, job_id):
        page = MyJobsPageForSearch(self.driver)
        page.open()
        page.jobs.delete_job(job_id)
        page.jobs.confirm_delete()
