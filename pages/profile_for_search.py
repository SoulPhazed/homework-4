from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException

from tests.general import Page, Component


class FreelancerPage(Page):
    PATH = '/freelancers/{}'

    def open_id(self, fl_id):
        self.PATH = self.PATH.format(fl_id)
        super().open()

    @property
    def info(self):
        return ProfileInfo(self.driver)


class AccountSettingsPage(Page):
    PATH = '/settings?tab=account'

    @property
    def form(self):
        return AccountSettingsForm(self.driver)


class AccountSettingsForm(Component):
    DATA_LOAD_STATUS = '//form[@id="mainSettingsForm"]//input[@name="email" and string-length(@value) > 0]'
    LAST_NAME_INPUT = '//form[@id="mainSettingsForm"]//input[@name="secondName"]'
    FIRST_NAME_INPUT = '//form[@id="mainSettingsForm"]//input[@name="firstName"]'

    def get_name(self):
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, self.DATA_LOAD_STATUS))
        )

        name_info = {
            "first_name": self.driver.find_element(By.XPATH, self.FIRST_NAME_INPUT).get_attribute("value"),
            "last_name": self.driver.find_element(By.XPATH, self.LAST_NAME_INPUT).get_attribute("value"),
        }
        return name_info


class FreelancerSettingsPage(Page):
    PATH = '/settings?tab=freelancer'

    @property
    def form(self):
        return FreelancerSettingsForm(self.driver)


class FreelancerSettingsForm(Component):
    DATA_LOAD_STATUS = '//input[@name="experienceLevelId" and @checked]'
    DESCRIPTION_INPUT = '//form[@id="descriptionForm"]//textarea[@name="overview"]'
    SKILLS_INPUT = '//form[@id="descriptionForm"]//input[@name="text field"]'
    SUBMIT = '//form[@id="descriptionForm"]//button[@type="submit"]'

    def set_description(self, description):
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, self.DATA_LOAD_STATUS))
        )
        descr_input = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.DESCRIPTION_INPUT))
        )
        descr_input.clear()
        descr_input.send_keys(description)

    def set_skills(self, skills):
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, self.DATA_LOAD_STATUS))
        )
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.SKILLS_INPUT))
        )
        for skill in skills:
            skills_input = self.driver.find_element(By.XPATH, self.SKILLS_INPUT)
            skills_input.clear()
            skills_input.send_keys(skill)
            skills_input.send_keys('\uE007')

    def submit(self):
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, self.DATA_LOAD_STATUS))
        )
        submit = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.SUBMIT))
        )
        submit.click()


class ProfileInfo(Component):
    LOAD_STATUS = '//span[@class="main-info__name" and string-length(normalize-space(text())) > 0]'
    NAME = '//span[@class="main-info__name"]'
    CITY = '//div[@class="main-info__info-column"]/*[1]'
    LEVEL = '//div[@class="main-info__info-column"]/*[2]'
    SPECIALITY = '//div[@class="main-info__info-column"]/*[3]'
    DESCRIPTION = '//p[@class="profile-description__text"]'
    SKILLS = '//div[contains(@class, "profile-skills__row")]/span'
    SKILL = SKILLS + '[{}]'

    def get_info(self):
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, self.LOAD_STATUS))
        )

        profile_descr = self.driver.find_element(By.XPATH, self.DESCRIPTION).text
        profile_descr = " ".join(profile_descr.split())
        if profile_descr == "Пока тут ничего нет":
            profile_descr = ""

        try:
            skills_raw = self.driver.find_elements(By.XPATH, self.SKILLS)
        except NoSuchElementException:
            skills_raw = []

        skills = []
        for i in range(1, len(skills_raw) + 1):
            skills.append(self.driver.find_element(By.XPATH, self.SKILL.format(i)).text)

        profile_data = {
            "id": self.driver.current_url.split('/')[-1],
            "first_name": self.driver.find_element(By.XPATH, self.NAME).text.split(" ")[0],
            "last_name": self.driver.find_element(By.XPATH, self.NAME).text.split(" ")[1],
            "level": self.driver.find_element(By.XPATH, self.LEVEL).text,
            "speciality": self.driver.find_element(By.XPATH, self.SPECIALITY).text,
            "country": self.driver.find_element(By.XPATH, self.CITY).text.split(", ")[0],
            "city": self.driver.find_element(By.XPATH, self.CITY).text.split(", ")[1],
            "description": profile_descr,
            "skills": skills,
        }

        return profile_data

    def get_id(self):
        WebDriverWait(self.driver, 10).until(
            ec.url_contains("freelancers")
        )

        return self.driver.current_url.split('/')[-1]
