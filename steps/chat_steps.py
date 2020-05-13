from tests.general import Step
from pages.chat_page import JobPageChat, ChatPage, ProposalPageChat
from pages.user_menu_page import UserMenuPage


class ChatSteps(Step):
    def __init__(self, driver, job_id):
        self.JOB_ID = job_id
        super().__init__(driver)

    def logout(self):
        page = UserMenuPage(self.driver)
        page.user_menu.toggle()
        page.user_menu.logout()

    def job_respond(self):
        page = JobPageChat(self.driver, self.JOB_ID)
        if "jobs" not in self.driver.current_url.split("/"):
            page.open()
        page.sidebar.to_respond()

    def get_proposal_id(self):
        page = JobPageChat(self.driver, self.JOB_ID)
        page.open()
        return page.proposals.get_proposal_id(self.JOB_ID)

    def fill_proposal_form(self, proposal_data):
        page = JobPageChat(self.driver, self.JOB_ID)
        page.sidebar.set_budget(proposal_data["budget"])
        page.sidebar.set_project_time(proposal_data["time"])
        page.sidebar.set_cover(proposal_data["cover"])

    def submit_proposal_form(self):
        page = JobPageChat(self.driver, self.JOB_ID)
        page.sidebar.submit()

    def confirm_candidate(self, proposal_id):
        page = ProposalPageChat(self.driver, proposal_id)
        page.open()
        page.proposal.confirm_candidate()

    def offer_contract(self, proposal_id):
        page = ProposalPageChat(self.driver, proposal_id)
        page.open()
        return page.proposal.offer_contract()

    def check_chat(self, proposal_id):
        page = ProposalPageChat(self.driver, proposal_id)
        page.open()
        return page.proposal.check_chat()

    def send_message(self, proposal_id, message):
        page = ChatPage(self.driver, proposal_id)
        page.open()
        page.chat.type_message(message)
        page.chat.send_message()

    def get_received_message(self, proposal_id):
        page = ChatPage(self.driver, proposal_id)
        page.open()
        return page.chat.get_first_received_message()

    def fill_contract_form(self, proposal_id, contract_info):
        page = ProposalPageChat(self.driver, proposal_id)
        page.proposal.set_budget(contract_info["budget"])
        page.proposal.set_project_time(contract_info["time"])

    def submit_contract_form(self, proposal_id):
        page = ProposalPageChat(self.driver, proposal_id)
        page.proposal.submit_contract_form()
