import os
from datetime import timezone
import datetime
import utils
import eventPublisher

# log level
log_level_map = {
    "info": "Info",
    "warn": "Warning",
    "error": "Error"
}


"""
  Takes level() map raw_event , map opts,map l, string app_vsn
  Send log to stdout and/or event bus

  ## Examples

      do_log(level, raw_event, opts, l)
       "Success"

      do_log(level, raw_event, opts, l)
     [log: "Some error", publish: "Some error"]

  """


# level is level(); opts is keyword(String.t())
def do_log(level, raw_event, opts, l, app_vsn):
    asyncc = None
    if(opts["async"] == None):
        if os.environ['async'] == None:
            asyncc = True
        else:
            asyncc = os.environ['async']
    else:
        asyncc = opts["async"]

    publish = True if(opts['publish'] == None) else opts['publish'] and (
        os.environ['publish_enabled'] not in [False, "false"])

    log = True if(opts["log"] == None) else opts["log"]

    res = parse_event(level, raw_event, l, app_vsn)

    if(log):
        log_event(res)

    # CODE AFTER THIS IS ELIXIR HEAVY


"""
  Takes level() ; raw_event map , l map , app_vasn string ;Parses the event into standard structure
  ## Examples
       publish_event(e) 
"""
# Parses the event into standard structure


def parse_event(level, raw_event, l, app_vsn):  # level()
    event_source = raw_event["event_source"] if(
        raw_event["event_source"] != None) else f'({l["app"]}) {l["file"]}: {l["line"]}: {l["m"]}.{l["f"]}/{l["a"]}'

    app_vsn = raw_event["app_vsn"] if(
        raw_event["app_vsn"] != None) else app_vsn
    component = raw_event["component"] if(
        raw_event["component"] != None) else os.environ['component']
    service = raw_event["service"] if(
        raw_event["service"] != None) else os.environ['service']
    event_value = raw_event["event_value"] if(
        raw_event["event_value"] != None) else raw_event["event_name"]
    # logger_metadata = Logger.metadata()
    # logger_metadata[:correlation_id]
    correlation_id = raw_event["correlation_id"]
    ou_id = raw_event["ou_id"]  # logger_metadata[:ou_id]
    x_request_id = raw_event["x_request_id"]  # logger_metadata[:x_request_id]
    reference_id = raw_event["reference_id"]  # logger_metadata[:reference_id]
    # logger_metadata[:reference_type]
    reference_type = raw_event["reference_type"]
    event_type = get_event_type(level, raw_event)
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    timestamp =raw_event["timestamp"]  if(raw_event["timestamp"] != None)  else utc_time
    details = raw_event["details"] if(
        type(raw_event["details"]) is dict) else dict({})
    service_category = raw_event["service_category"] if(
        raw_event["service_category"] != None) else os.environ('service_category')

    return {
        "app_vsn": app_vsn,
        "eid": utils.uuid4(),
        "component": component,
        "service": service,
        "event_value": event_value,
        "correlation_id": correlation_id,
        "ou_id": ou_id,
        "x_request_id": x_request_id,
        "timestamp": timestamp,
        "details": details,
        "reference_id": reference_id,
        "reference_type": reference_type,
        "event_type": event_type,
        # "level": level,
        "level_value": log_level_map[level],
        "service_category": service_category,
        "event_source": event_source,
        "log_version": raw_event["log_version"]
    }


"""
  Takes map ; publishes event to console

  ## Examples
       publish_event(e) 
"""


def log_event(e):
    # timestamp = IdfyInstrumenter.format_timestamp(e[timestamp, :log) #HOW TO DO IN PYTHON
    message = f'{e["reference_id"]}: {e["service"]} -> {e["event_type"]} - {e["event_value"]}'

    event = {
        "app_vsn": e["app_vsn"],
        "eid": e["eid"],
        #   "timestamp" : timestamp,
        "x_request_id": e["x_request_id"],
        "event_source": e["event_source"],
        "log_level": e["level_value"],
        "service_category": e["service_category"],
        "ou_id": e["ou_id"],
        "correlation_id": e["correlation_id"],
        "reference_id": e["reference_id"],
        "reference_type": e["reference_type"],
        "component": e["component"],
        "service": e["service"],
        "event_type": e["event_type"],
        "event_name": e["event_value"],
        #   "details" : Jason.encode!(e[details),
        "log_version": e["log_version"],
        "message": message
    }

   # Logger.log(e.level, fn -> {"", event} end)
    print(event)


"""
  Takes map ; publishes event to event bus

  ## Examples
       publish_event(e) 
"""


def publish_event(e):
    # timestamp = IdfyInstrumenter.format_timestamp(e[timestamp, :publish) #HOW TO DO IN PYTHON
    event = {
        "app_vsn": e["app_vsn"],
        "eid": e["eid"],
        # "timestamp" : timestamp,
        "x_request_id": e["x_request_id"],
        "event_source": e["event_source"],
        "log_level": e["level_value"],
        "service_category": e["service_category"],
        "ou_id": e["ou_id"],
        "correlation_id": e["correlation_id"],
        "reference_id": e["reference_id"],
        "reference_type": e["reference_type"],
        "component": e["component"],
        "service": e["service"],
        "event_type": e["event_type"],
        "event_value": e["event_value"],
        "log_version": e["log_version"],
        "details": e["details"]
    }

    #   publisher =
    #   Application.get_env(:idfy_instrumenter, :publisher) || IdfyInstrumenter.RMQ.EventsPublisher

    # publisher.publish_message(event, generate_routing_key(e))

    eventPublisher.publish_message(event, generate_routing_key(e))


"""
  Takes map ; returns  routing key for event bus

  ## Examples

       generate_routing_key(e) 
      "routing_key"
"""


def generate_routing_key(e):
    event_source = utils.make_routing_key_safe(
        utils.event_source_routing_key(e["event_source"]))
    service_category = utils.make_routing_key_safe(e["service_category"])
    component = utils.make_routing_key_safe(e["component"])
    service = utils.make_routing_key_safe(e["service"])
    event_type = utils.make_routing_key_safe(e["event_type"])
    log_version = utils.make_routing_key_safe(e["log_version"])

    return f'{e["level_value"]}.{event_source}.{log_version}.{service_category}.{component}.{service}.{event_type}'



"""
  Takes level string event_map map and  returns  string

  ## Examples

       get_event_type("error",{}) 
      "routing_key"

"""


def get_event_type(level, event_map):
    if(level == "error"):
        return "Exception" if (event_map["event_type"] is None) else event_map["event_type"]
    if(level == "warn"):
        return "Warning" if (event_map["event_type"] is None) else event_map["event_type"]
    else:
        return event_map["event_type"]


########################DRIVER CODE############################
e = {
    "app_vsn": "app_vsn",
    "eid": "eid",
    "timestamp": "timestamp",
    "x_request_id": "x_request_id",
    "event_source": "event_source",
    "log_level": "level_value",
    "service_category": "service_category",
    "ou_id": "ou_id",
    "correlation_id": "correlation_id",
    "reference_id": "reference_id",
    "reference_type": "reference_type",
    "component": "component",
    "service": "service",
    "event_type": "event_type",
    "event_value": "event_value",
    "log_version": "log_version",
    "details": "details",
    "level_value": "level_value"

}


publish_event(e)
