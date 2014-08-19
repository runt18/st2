from st2common import log as logging
from st2common.models.api.reactor import TriggerAPI
from st2common.persistence.reactor import Trigger

LOG = logging.getLogger(__name__)


def _get_trigger_db(type_name=None, parameters=None):
    try:
        return Trigger.query(type__name=type_name,
                             parameters=parameters).first()
    except ValueError as e:
        LOG.debug('Database lookup for type[\'name\']="%s" parameters="%s" resulted ' +
                  'in exception : %s.', type_name, parameters, e, exc_info=True)
        return None


def _get_trigger_db_by_name(name):
    try:
        return Trigger.get_by_name(name)
    except ValueError as e:
        LOG.debug('Database lookup for name="%s" resulted ' +
                  'in exception : %s.', name, e, exc_info=True)
        return None


def get_trigger_db(trigger):
    if type(trigger) == str:
        return _get_trigger_db_by_name(trigger)
    if isinstance(trigger, dict):
        name = trigger.get('name', None)
        if name:
            return _get_trigger_db_by_name(name)
        return _get_trigger_db(type_name=trigger['type']['name'],
                               parameters=trigger['parameters'])
    if isinstance(trigger, object):
        if hasattr(trigger, 'name') and trigger.name:
            trigger_db = _get_trigger_db_by_name(trigger.name)
            if not trigger_db:
                trigger_db = _get_trigger_db(type_name=trigger.type,
                                             parameters=trigger.parameters)
            if trigger_db:
                LOG.debug('Found matching TriggerDB=%s for trigger=%s', trigger_db, trigger)
    return trigger_db


def create_trigger_db(trigger):
    trigger_api = trigger
    if isinstance(trigger, dict):
        trigger_api = TriggerAPI(**trigger)
    trigger_db = get_trigger_db(trigger_api)
    if not trigger_db:
        trigger_db = TriggerAPI.to_model(trigger_api)
        LOG.debug('verified trigger and formulated TriggerDB=%s', trigger_db)
        trigger_db = Trigger.add_or_update(trigger_db)
    return trigger_db
