from pecan import expose
from webob.exc import status_map

from st2reactorcontroller.controllers.triggers import TriggerTypeController, TriggerController, \
    TriggerInstanceController
from st2reactorcontroller.controllers.rules import RuleController, RuleEnforcementController


class RootController(object):

    triggertypes = TriggerTypeController()
    triggers = TriggerController()
    triggerinstances = TriggerInstanceController()
    rules = RuleController()
    ruleenforcements = RuleEnforcementController()

    @expose(generic=True, template='index.html')
    def index(self):
        return dict()

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
