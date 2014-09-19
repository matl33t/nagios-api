#!/usr/bin/python
import json
def status_to_s(state):
    status_map = {"0": "OK", "1": "WARN", "2": "CRIT", "3": "UNK"}
    return status_map[state]

class HostOrService:
    def __init__(self, name, attributes):
        self.name = name
        self.current_state = status_to_s(attributes['current_state'])
        self.plugin_output = attributes['plugin_output']
        self.notifications_enabled = attributes['notifications_enabled']
        self.last_check = attributes['last_check']
        self.last_notification = attributes['last_notification']
        self.active_checks_enabled = attributes['active_checks_enabled']
        self.problem_has_been_acknowledged = attributes['problem_has_been_acknowledged']
        self.last_hard_state = attributes['last_hard_state']
        self.scheduled_downtime_depth = attributes['scheduled_downtime_depth']
        self.performance_data = attributes['performance_data']
        self.last_state_change = attributes['last_state_change']
        self.current_attempt = attributes['current_attempt']
        self.max_attempts = attributes['max_attempts']

class Host(HostOrService):
    def __init__(self, name, attributes):
        HostOrService.__init__(self, name, attributes)
        self.services = {}
    def attach_service(self, svc):
        '''Attach a Service to this Host.'''
        self.services[svc.service] = svc

class Service(HostOrService):
    def __init__(self, name, attributes, host = None):
        HostOrService.__init__(self, name, attributes)
        self.host = host
    def attach_host(self, host):
        '''Attach a Service to this Host.'''
        self.host = host
    def pp(self, opts = None):
        print "%s\t%s\t%s\t%s\t%s\t%s" % (
          self.host.ljust(25),
          self.name[:35].ljust(35),
          self.plugin_output[:35].ljust(35),
          self.current_state,
          self.problem_has_been_acknowledged == "1" and "ACK" or " ",
          self.notifications_enabled == "1" and " " or "MUTED",
        )


