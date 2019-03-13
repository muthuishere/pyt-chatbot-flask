from chatterbot.logic import LogicAdapter


class InternalAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['INC']
        for stm in statement.text.split():
            for word in words:
                if stm.find(word) == 0:
                    print("found!")
                    return True
        return False

    def process(self,statement, additional_response_selection_parameters):
        from chatterbot.conversation import Statement

        # call other API for finding account
        foundaccount = True;
        account = "57441222-002 8"

        if foundaccount:
            confidence = 1
        else:
            confidence = 0

        # For this example, we will just return the input as output
        selected_statement = Statement(text="Is your account number {} ?".format(account))
        selected_statement.confidence = confidence

        return selected_statement
#Is your account number 57441222-002 8 ?