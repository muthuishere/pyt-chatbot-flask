from incidents.incident import Incident
import datetime


class IncidentService:
    def __init__(self):
        super().__init__()

    def getIncidentStatus(self, incidentno):
        # TODO Call Database and return status
        return self.__getMockedStatus(incidentno)

    def __getMockedStatus(self, incidentno):
        if(incidentno.endswith("1")):
            return self.__getFinishedStatus(incidentno)
        elif (incidentno.endswith("2")):
            return self.__getEscalataedStatus(incidentno)
        elif (incidentno.endswith("3")):
            return self.__getInProgressStatus(incidentno)
        elif (incidentno.endswith("4")):
            return self.__getAssignedStatus(incidentno)
        else:
            return None

    def __getFinishedStatus(self, incidentno):
        return Incident("John Doe", incidentno, "Finished", datetime.datetime.now(),
                        "Access to email is restablished but it needs 3 hours to sync in all servers. ")

    def __getEscalataedStatus(self, incidentno):
        return Incident("John Doe", incidentno, "Finished", datetime.datetime.now(),
                        "Ticket was escalated to level III support due critical change in the database.")

    def __getAssignedStatus(self, incidentno):
        return Incident("John Doe", incidentno, "Assigned", datetime.datetime.now(),
                        "User contacted and we're going to the location informed.")

    def __getInProgressStatus(self, incidentno):
        today = datetime.datetime.now()
        tomorrow = today + datetime.timedelta(days=1)
        return Incident("John Doe", incidentno, "In Progress", tomorrow,
                        "We're working to restablish license to e-mail.")
