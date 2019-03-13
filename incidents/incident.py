from datetime import date


class Incident:
    customer: str
    ticket: str
    status: str
    duedate: date
    lastnotes: str

    def __init__(self, customer: str, ticket: str, status: str,duedate: date,lastnotes: str):
        self.customer = customer
        self.ticket = ticket
        self.status = status
        self.duedate = duedate
        self.lastnotes = lastnotes


    def tostring(self) -> str:
        return  "Customer {}, ticket {}, status: {}, due date: {}. Last notes: {}" .format(self.customer,self.ticket,self.status,self.duedate,self.lastnotes)

