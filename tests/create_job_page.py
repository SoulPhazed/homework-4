
class CreateJobPage(Page):
    PATH = '/new-job'
    CREATE_BTN = '//a[@data-test-id="top-new-job"]'

    @property
    def form(self):
        return JobForm(self.driver)

    def open_form(self):
        Waiter.wait_by_xpath(self.driver, self.CREATE_BTN).click()