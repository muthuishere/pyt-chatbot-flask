from chatterbot.logic import LogicAdapter
import re

from incidents.incident_service import IncidentService


class BotAddressAdapter(LogicAdapter):
    incidentService = IncidentService()

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        txt = statement.text
        return self.hasAddress(txt) or self.hasConfirmation(txt)

    def attachIdleText(self):
        return "#TIMED#any other questions?"

    def hasConfirmation(self, txt):
        if ("I do" in txt or "I confirm" in txt or "I agree" in txt):
            return True
        else:
            return False

    def getAddressRegex(self,txt):
        return re.search(r'[0-9][0-9][0-9][0-9] [a-zA-Z] [0-9][0-9][0-9][0-9].+[0-9][0-9][0-9][0-9][0-9]', txt,
                         re.M | re.I)

    def hasAddress(self, txt):
        searchObj = self.getAddressRegex(txt)

        if searchObj:
            return True
        else:
            return False

    def createincident(self):
        # Get from database , Currently dummy
        return "12345678"

    def process(self, statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        confidence = 0
        txt = statement.text
        if self.hasConfirmation(txt):
            confidence = 1
            response = 'Your address has been changed. Your request number is: ' + self.createincident() + self.attachIdleText()
        else:
            searchObj = self.getAddressRegex(txt)
            address = None

            if searchObj:
                address = searchObj.group()
                if ("current address" in txt):
                    confidence = 0.7
                    response = "I've got your information. What's the new address? "
                else:
                    confidence = 0.7
                    response = "Do you confirm your address change to:" + address

        selected_statement = Statement(text=response)
        selected_statement.confidence = confidence

        return selected_statement
