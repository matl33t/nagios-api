#!/usr/bin/python

import sys


def time_to_seconds(inp):
    '''Possibly convert a time written like "2h" or "50m" into seconds.

    '''
    match = re.match(r'^(\d+)([wdhms])?$', inp)
    if match is None:
        return None
    val, denom = match.groups()
    if denom is None:
        return int(val)
    multiplier = {'w': 604800, 'd': 86400, 'h': 3600, 'm': 60, 's': 1}[denom]
    return int(val) * multiplier

def trim(docstring):
    '''This is taken from PEP 257 for docstring usage. I'm duplicating
    it here so I can use it to preparse docstrings before sending them
    to OptionParser. Otherwise, I can either not indent my docstrings
    (in violation of the PEP) or I can have the usage outputs be
    indented.

    '''
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def status_to_s(state):
    status_map = {"0": "OK", "1": "WARN", "2": "CRIT", "3": "UNK"}
    return status_map[state]

class HostOrService:
    attrs = ['current_state', 'plugin_output',
            'notifications_enabled', 'last_check', 'last_notification',
            'active_checks_enabled', 'problem_has_been_acknowledged',
            'last_hard_state', 'scheduled_downtime_depth', 'performance_data',
            'last_state_change', 'current_attempt', 'max_attempts']

    def __init__(self, name, attributes):
        self.name = name.decode('utf-8')
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
        self.host = host.decode('utf-8')
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


