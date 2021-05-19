import utils;




"""
  Takes map ; returns  routing key for event bus

  ## Examples

       generate_routing_key(e) 
      "routing_key"
"""
def generate_routing_key(e):
    event_source = utils.make_routing_key_safe(utils.event_source_routing_key(e[event_source]))
    service_category = utils.make_routing_key_safe(e[service_category])
    component = utils.make_routing_key_safe(e[component])
    service = utils.make_routing_key_safe(e[service])
    event_type = utils.make_routing_key_safe(e[event_type])
    log_version = utils.make_routing_key_safe(e[log_version])

    return f'{e[level_value]}.{event_source}.{log_version}.{service_category}.{component}.{service}.{event_type}'


"""
  Takes level string event_map map and  returns  string

  ## Examples

       get_event_type("error",{}) 
      "routing_key"

"""
def get_event_type(level, event_map):
    if(level == "error"):
        return "Exception"  if (event_map["event_type"] is None) else event_map["event_type"] 
    if(level == "warn"):
        return "Warning"  if (event_map["event_type"] is None) else event_map["event_type"] 
    else:
        return event_map["event_type"]




