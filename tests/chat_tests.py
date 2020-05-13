import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote
from steps.job_for_search import JobStepsForSearch
from steps.auth_steps import AuthSteps
from steps.chat_steps import ChatSteps


class ChatTest(unittest.TestCase):
    ROLE = None

    AUTH_ATTEMPTS = 5

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

        for i in range(self.AUTH_ATTEMPTS):
            status = auth_steps.login_as_client()
            if status is True:
                break

        self.ROLE = "client"
        job_steps = JobStepsForSearch(self.driver)
        job_steps.create_custom(self.JOB_DATA)

        self.JOB_DATA["id"] = job_steps.get_job_id()

    def tearDown(self):
        if self.ROLE == "freelancer":
            chat_steps = ChatSteps(self.driver, self.JOB_DATA["id"])
            chat_steps.logout()
            self.ROLE = None

        if self.ROLE is None:
            auth_steps = AuthSteps(self.driver)
            for i in range(self.AUTH_ATTEMPTS):
                status = auth_steps.login_as_client()
                if status is True:
                    break

        my_jobs = JobStepsForSearch(self.driver)
        my_jobs.delete_job(self.JOB_DATA["id"])

        self.driver.quit()

    def go_to_chat(self):
        PROPOSAL = {
            "budget": "10000",
            "time": "1",
            "cover": "Cover from Selenium"
        }

        chat_steps = ChatSteps(self.driver, self.JOB_DATA["id"])
        auth_steps = AuthSteps(self.driver)

        if self.ROLE == "client":
            chat_steps.logout()
            self.ROLE = None

        if self.ROLE is None:
            for i in range(self.AUTH_ATTEMPTS):
                status = auth_steps.login_as_freelancer()
                if status is True:
                    break
            self.ROLE = "freelancer"

        chat_steps.job_respond()
        chat_steps.fill_proposal_form(PROPOSAL)
        chat_steps.submit_proposal_form()

        chat_steps.logout()
        self.ROLE = None
        for i in range(self.AUTH_ATTEMPTS):
            status = auth_steps.login_as_client()
            if status is True:
                break
        self.ROLE = "client"

        self.PROPOSAL_ID = chat_steps.get_proposal_id()
        chat_steps.confirm_candidate(self.PROPOSAL_ID)

    def test_chat_appearance(self):
        self.go_to_chat()
        chat_steps = ChatSteps(self.driver, self.JOB_DATA["id"])

        self.assertTrue(chat_steps.check_chat(self.PROPOSAL_ID))

    def test_message_sending(self):
        MESSAGE = "Hello from Selenium!"
        self.go_to_chat()
        chat_steps = ChatSteps(self.driver, self.JOB_DATA["id"])
        auth_steps = AuthSteps(self.driver)
        chat_steps.send_message(self.PROPOSAL_ID, MESSAGE)

        chat_steps.logout()
        self.ROLE = None
        for i in range(self.AUTH_ATTEMPTS):
            status = auth_steps.login_as_freelancer()
            if status is True:
                break
        self.ROLE = "freelancer"

        received_msg = chat_steps.get_received_message(self.PROPOSAL_ID)

        self.assertTrue(received_msg == MESSAGE)

    def test_chat_closing(self):
        CONTRACT_INFO = {
            "budget": "10000",
            "time": "1"
        }
        self.go_to_chat()
        chat_steps = ChatSteps(self.driver, self.JOB_DATA["id"])
        chat_steps.offer_contract(self.PROPOSAL_ID)
        chat_steps.fill_contract_form(self.PROPOSAL_ID, CONTRACT_INFO)
        chat_steps.submit_contract_form(self.PROPOSAL_ID)

        self.assertFalse(chat_steps.check_chat(self.PROPOSAL_ID))
