import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from tests.general import Page, Component


class ChatPage(Page):
    PATH = '/proposals/{}'

    def __init__(self, driver, proposal_id):
        self.PATH = self.PATH.format(proposal_id)
        super().__init__(driver)

    @property
    def chat(self):
        return ChatWindow(self.driver)


class ChatWindow(Component):
    CHAT_WINDOW = '//div[@class="fwork-chat"]'
    CHAT_INPUT = CHAT_WINDOW + '//textarea[@class="message-textarea"]'
    CHAT_SEND = CHAT_WINDOW + '//button[contains(@class, "send-message-button")]'
    CHAT_COMPANION_MESSAGE = CHAT_WINDOW + '//div[normalize-space(@class)="content-wrapper"]//span[@class="message-text"]'

    def type_message(self, message):
        try:
            input_msg = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, self.CHAT_INPUT))
            )
            input_msg.clear()
            input_msg.send_keys(message)
        except TimeoutException:
            print("type_message: chat is not available")

    def send_message(self):
        try:
            send_btn = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, self.CHAT_SEND))
            )
            send_btn.click()
        except TimeoutException:
            print("send_message: chat is not available")

    def get_first_received_message(self):
        try:
            message = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, self.CHAT_COMPANION_MESSAGE))
            )
            return message.text
        except TimeoutException:
            print("get_first_received_message: chat is not available")
            return None


class JobPageChat(Page):
    PATH = '/jobs/{}'

    def __init__(self, driver, job_id):
        self.PATH = self.PATH.format(job_id)
        super().__init__(driver)

    @property
    def sidebar(self):
        return JobSidebar(self.driver)

    @property
    def proposals(self):
        return JobProposals(self.driver)


class JobSidebar(Component):
    LOAD_STATUS = '//h2[contains(@class, "job-details_title") and string-length(text()) > 0]'
    RESPONSE = '//div[contains(@class, "job-details-sidebar")]//button[@type="submit"]'
    PROPOSAL_BUDGET = '//form[@id="addProposal"]//input[@name="paymentAmount"]'
    PROPOSAL_TIME_SELECT = '//div[./select[@name="timeEstimation"]]/div/div'
    PROPOSAL_TIME_ITEM = PROPOSAL_TIME_SELECT + '//li[@data-val="{}"]'
    PROPOSAL_COVER = '//form[@id="addProposal"]//textarea[@name="coverLetter"]'
    PROPOSAL_SUBMIT = '//form[@id="addProposal"]//button[@type="submit"]'

    def to_respond(self):
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, self.LOAD_STATUS))
        )
        button = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.RESPONSE))
        )
        button.click()

    def set_budget(self, budget):
        budget_input = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.PROPOSAL_BUDGET))
        )
        budget_input.clear()
        budget_input.send_keys(budget)

    def set_project_time(self, proj_time):
        time_select = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.PROPOSAL_TIME_SELECT))
        )
        time_select.click()
        time_item = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.PROPOSAL_TIME_ITEM.format(proj_time)))
        )
        time_item.click()
        time.sleep(1)

    def set_cover(self, cover_text):
        cover_input = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.PROPOSAL_COVER))
        )
        cover_input.clear()
        cover_input.send_keys(cover_text)

    def submit(self):
        proposal_submit = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.PROPOSAL_SUBMIT))
        )
        proposal_submit.click()


class JobProposals(Component):
    PROPOSALS = '//div[@class="proposals-list__link"]//a[@class="link"]'
    PROPOSAL = PROPOSALS + '[{}]'

    def get_proposal_id(self, job_id):
        proposals = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_all_elements_located((By.XPATH, self.PROPOSALS))
        )

        if len(proposals) >= 1:
            for i in range(1, len(proposals) + 1):
                proposal = self.driver.find_element(By.XPATH, self.PROPOSAL.format(i))
                proposal_id = proposal.get_attribute("href").split('/')[-1]
                proposal.click()
                proposal_page = ProposalPageChat(self.driver, proposal_id)
                if proposal_page.proposal.get_job_id() == job_id:
                    break
                else:
                    proposal_id = -1
        elif len(proposals) == 0:
            proposal_id = -1

        return proposal_id


class ProposalPageChat(Page):
    PATH = '/proposals/{}'

    def __init__(self, driver, proposal_id):
        self.PATH = self.PATH.format(proposal_id)
        super().__init__(driver)

    @property
    def proposal(self):
        return ProposalChat(self.driver)


class ProposalChat(Component):
    JOB_LINK = '//div[@class="job-details__inner-item"]//a[contains(@href, "jobs")]'
    SUBMIT_CANDIDATE = '//div[contains(@class, "proposal__action-buttons")]//button[@type="submit"]'
    CHAT_WINDOW = '//div[@class="fwork-chat"]'

    CONTRACT_BUDGET = '//form[@id="newContract"]//input[@name="paymentAmount"]'
    CONTRACT_TIME_SELECT = '//form[@id="newContract"]//div[./select[@name="timeEstimation"]]/div/div'
    CONTRACT_TIME_ITEM = CONTRACT_TIME_SELECT + '//li[@data-val="{}"]'
    CONTRACT_SUBMIT = '//form[@id="newContract"]//button[@type="submit"]'

    def get_job_id(self):
        link = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, self.JOB_LINK))
        )

        return link.get_attribute("href").split('/')[-1]

    def confirm_candidate(self):
        button = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.SUBMIT_CANDIDATE))
        )

        button.click()

    def set_budget(self, budget):
        try:
            # Avoiding bug with input disappear
            time.sleep(1.5)

            budget_input = WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, self.CONTRACT_BUDGET))
            )
            budget_input.clear()
            budget_input.send_keys(budget)
        except TimeoutException:
            print("set_budget: contract is not available")

    def set_project_time(self, proj_time):
        try:
            time_select = WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, self.CONTRACT_TIME_SELECT))
            )
            time.sleep(5)
            time_select.click()
            time_item = WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, self.CONTRACT_TIME_ITEM.format(proj_time)))
            )
            time_item.click()
            time.sleep(1)
        except TimeoutException:
            print("set_project_time: contract is not available")

    def submit_contract_form(self):
        try:
            contract_submit = WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, self.CONTRACT_SUBMIT))
            )
            contract_submit.click()
        except TimeoutException:
            print("submit_contract_form: contract is not available")

    def offer_contract(self):
        status = self.check_chat()
        if status is False:
            return False

        button = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.SUBMIT_CANDIDATE))
        )
        button.click()

        return True

    def check_chat(self):
        try:
            WebDriverWait(self.driver, 5).until(
                ec.visibility_of_element_located((By.XPATH, self.CHAT_WINDOW))
            )
        except TimeoutException:
            return False

        return True
