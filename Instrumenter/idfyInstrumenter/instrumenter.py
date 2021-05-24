import os
from datetime import timezone
import datetime
from .utils import make_routing_key_safe, event_source_routing_key, uuid4
from .eventPublisher import PublishMessage
import threading


# log level
log_level_map = {
    "info": "Info",
    "warn": "Warning",
    "error": "Error"
}


def publish_status(res):
    publish_res = publish_event(res)
    if(publish_res == "PunlishedToRabbitMQ"):
        print("Published To Rabbit MQ")
    else:
        print("Error Publishing to RabbitMQ")


def error_status(res):
    errors = []
    publish_res = publish_event(res)
    if(publish_res == "PunlishedToRabbitMQ"):
        errors = errors
    else:
        errors = errors + [e]
    if (errors.len == 0):
        print("Sucess")
    else:
        print("Error")


"""
  ## Parameters
   - level: 'info', 'warn', 'error'
   - raw_event: map containing the actual event
   - opts:{async:"T/F","publish":T/F,"log":T/f}
            async(default true) : T to publish to event bus
            publish:(default false):T to publish to event bus
            log(defatul true): T to publish to event bus
    
    -l : l is a map with following keys
         {"app","file","line","m","f","a"}
    -app_vsn: app version given by env var 
  ## Examples

      do_log("info", event, {}, {},"1.11")
       "Success"

      do_log(level, raw_event, opts, l)
       "Error"

  """


def do_log(level, raw_event, opts, l, app_vsn):
    log = True
    if("log" not in opts):
        log = True
    else:
        log = opts["log"]

    asyncc = True
    if("async" not in opts):
        if os.environ['async'] == None:
            asyncc = True
        else:
            asyncc = os.environ['async']
    else:
        asyncc = opts["async"]

    publish = False
    if("publish" not in opts):
        publish = False
    else:
        publish = opts['publish']

    res = parse_event(level, raw_event, l, app_vsn)
    if(log):
        print("RESULT LOGGED TO CONSOLE")
        log_event(res)

    if (publish == True):
        if (asyncc == True):
            # https://medium.com/velotio-perspectives/an-introduction-to-asynchronous-programming-in-python-af0189a88bbb
            t1 = threading.Thread(target=publish_status, args=(res,))
            t1.start()
            t1.join()
            # publish_status(res)

        else:
            error_status(res)
    else:
        print("Sucsss")


"""
   ## Parameters
   - level: 'info', 'warn', 'error'
   - raw_event: map containing the actual event
    -l : l is a map with following keys
         {"app","file","line","m","f","a"}
    -app_vsn: app version given by env var 
  ## Examples
       parse_event("info",event,{}."1.1") 
"""
# Parses the event into standard structure


def parse_event(level, raw_event, l, app_vsn):  # level()
    event_source = raw_event["event_source"] if(
        "event_source" in raw_event) else f'({l["app"]}) {l["file"]}: {l["line"]}: {l["m"]}.{l["f"]}/{l["a"]}'

    app_vsn = raw_event["app_vsn"] if("app_vsn" in raw_event) else app_vsn
    component = raw_event["component"] if(
        "component" in raw_event) else os.environ['component']
    service = raw_event["service"] if(
        "service" in raw_event) else os.environ['service']
    event_value = raw_event["event_value"] if(
        "event_value" in raw_event) else raw_event["event_name"]
    # logger_metadata = Logger.metadata()
    correlation_id = raw_event["correlation_id"] if(
        "correlation_id" in raw_event) else "correlation_id"  # logger_metadata[:correlation_id]
    ou_id = raw_event["ou_id"] if(
        "ou_id" in raw_event) else "ou_id"   # logger_metadata[:ou_id]
    x_request_id = raw_event["x_request_id"] if(
        "x_request_id" in raw_event) else "x_request_id"  # logger_metadata[:x_request_id]
    # logger_metadata[:reference_id]
    reference_id = raw_event["reference_id"] if("reference_id" in raw_event) else "reference_id"
    reference_type = raw_event["reference_type"] if(
        "reference_type" in raw_event) else "reference_type"    # logger_metadata[:reference_type]
    event_type = get_event_type(level, raw_event)
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    timestamp = raw_event["timestamp"] if(
        "timestamp" in raw_event) else utc_time
    details = raw_event["details"] if(
        type(raw_event["details"]) is dict) else dict({})
    service_category = raw_event["service_category"] if(
        "service_category" in raw_event) else os.environ('service_category')

    return {
        "app_vsn": app_vsn,
        "eid": uuid4(),
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
        "level": level,
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

publishMessage = PublishMessage()


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

    try:
        publishMessage.publish_message(event, generate_routing_key(e))
        return "PunlishedToRabbitMQ"
    except Exception as e:
        return e


"""
  Takes map ; returns  routing key for event bus

  ## Examples

       generate_routing_key(e) False
      "routing_key"
"""


def generate_routing_key(e):
    event_source = make_routing_key_safe(
        event_source_routing_key(e["event_source"]))
    service_category = make_routing_key_safe(e["service_category"])
    component = make_routing_key_safe(e["component"])
    service = make_routing_key_safe(e["service"])
    event_type = make_routing_key_safe(e["event_type"])
    log_version = make_routing_key_safe(e["log_version"])

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
