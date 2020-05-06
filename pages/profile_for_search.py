from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from tests.general import Page, Component


class FreelancerPage(Page):
    PATH = '/freelancers/{}'
    CREATE_BTN = '//a[contains(@href,"/new-job")]'

    def open_id(self, fl_id):
        self.PATH = self.PATH.format(fl_id)
        super().open()

    @property
    def info(self):
        return ProfileInfo(self.driver)


class ProfileInfo(Component):
    LOAD_STATUS = '//span[@class="main-info__name" and string-length(normalize-space(text())) > 0]'
    NAME = '//span[@class="main-info__name"]'
    CITY = '//div[@class="main-info__info-column"]/*[1]'
    LEVEL = '//div[@class="main-info__info-column"]/*[2]'
    SPECIALITY = '//div[@class="main-info__info-column"]/*[3]'

    def get_info(self):
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, self.LOAD_STATUS))
        )

        profile_data = {
            "id": self.driver.current_url.split('/')[-1],
            "first_name": self.driver.find_element(By.XPATH, self.NAME).text.split[" "][0],
            "last_name": self.driver.find_element(By.XPATH, self.LEVEL).text.split[" "][1],
            "level": self.driver.find_element(By.XPATH, self.SPECIALITY).text,
        }

        return profile_data

    def get_id(self):
        WebDriverWait(self.driver, 10).until(
            ec.url_contains("freelancers")
        )

        return self.driver.current_url.split('/')[-1]
