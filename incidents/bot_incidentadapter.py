from chatterbot.logic import LogicAdapter
import re

from incidents.incident_service import IncidentService


class IncidentAdapter(LogicAdapter):
    incidentService = IncidentService()

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['INC']
        for stm in statement.text.split():
            for word in words:
                if stm.find(word) == 0:
                    return True

        txt = statement.text


        #
        if(self.hasOnlyPhoneNumber(txt)):
            return True

        return False

    def getPhoneNumberRegex(self, txt):
        # 358-895-7455
        return re.search(r'[0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]', txt,
                         re.M | re.I)

    def hasOnlyPhoneNumber(self, txt):
        searchObj = self.getPhoneNumberRegex(txt)

        if searchObj:
            phoneNo = searchObj.group()
            resultval = txt.replace(phoneNo, "").strip()

            return len(resultval) == 0
        else:
            return False

    def attachIdleText(self):
        return "#TIMED#do you have any other question?"

    def getIncident(self, statementText):

        print("getIncident", statementText)
        searchObj = re.search(r'(INC[0-9]+)', statementText, re.M | re.I)
        incidentNo = None

        if searchObj:
            incidentNo = searchObj.group()
        return incidentNo

    def process(self, statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        txt = ''
        if (self.hasOnlyPhoneNumber(statement.text)):
            confidence = 1
            # TODO modify for only phone number stuff
            txt = "I've opened ticket INC20180402 for you. The time frame for assigning this ticket is 30 min. You should receive a call after that. You also can come back and ask me the status of your ticket if you want providing the ticket number."
        else:
            incidentNo = self.getIncident(statement.text)

            if incidentNo:
                confidence = 1
                incidentStatus = IncidentAdapter.incidentService.getIncidentStatus(incidentNo)
                if incidentStatus:
                    txt = 'This is the status of your ticket:' + incidentStatus.tostring() + self.attachIdleText()
                else:
                    txt = "Sorry, I can't find this number, please try again on call support 800-555-555"
            else:
                confidence = 0
        selected_statement = Statement(text=txt)
        selected_statement.confidence = confidence

        return selected_statement
