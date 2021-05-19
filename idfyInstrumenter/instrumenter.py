import utils
import eventPiblisher



"""
  Takes map ; publishes event to console

  ## Examples
       publish_event(e) 
"""
def log_event(e): 
    # timestamp = IdfyInstrumenter.format_timestamp(e[timestamp, :log) #HOW TO DO IN PYTHON
    message = f'{e[reference_id]}: {e[service]} -> {e[event_type]} - {e[event_value]}'

    event = {
      "app_vsn" : e[app_vsn],
      "eid" : e[eid],
    #   "timestamp" : timestamp,
      "x_request_id" : e[x_request_id],
      "event_source" : e[event_source],
      "log_level" : e[level_value],
      "service_category" : e[service_category],
      "ou_id" : e[ou_id],
      "correlation_id" : e[correlation_id],
      "reference_id" : e[reference_id],
      "reference_type" : e[reference_type],
      "component" : e[component],
      "service" : e[service],
      "event_type" : e[event_type],
      "event_name" : e[event_value],
    #   "details" : Jason.encode!(e[details),#HOW TO DO IN PYTHON 
      "log_version" : e[log_version],
      "message" : message
    }

    print(event)   #HOW TO DO IN PYTHON 




"""
  Takes map ; publishes event to event bus

  ## Examples
       publish_event(e) 
"""
def publish_event(e):
    # timestamp = IdfyInstrumenter.format_timestamp(e[timestamp, :publish) #HOW TO DO IN PYTHON
      event = {
      "app_vsn" : e[app_vsn],
      "eid" : e[eid],
      # "timestamp" : timestamp,
      "x_request_id" : e[x_request_id],
      "event_source" : e[event_source],
      "log_level" : e[level_value],
      "service_category" : e[service_category],
      "ou_id" : e[ou_id],
      "correlation_id" : e[correlation_id],
      "reference_id" : e[reference_id],
      "reference_type" : e[reference_type],
      "component" : e[component],
      "service" : e[service],
      "event_type" : e[event_type],
      "event_value" : e[event_value],
      "log_version" : e[log_version],
      "details" : e[details]
      }

      eventPiblisher.publish_message(event,generate_routing_key(e))




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




