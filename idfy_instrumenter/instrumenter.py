import os
from datetime import timezone
import datetime

import json
import logging
from .utils import make_routing_key_safe, event_source_routing_key, uuid4
from .event_publisher import Publisher
import threading


log_level_map = {
    "info": "Info",
    "warn": "Warning",
    "error": "Error"
}


def log_level_generator(level):
    if(level == "info"):
        return logging.INFO  # 20
    if(level == "warn"):
        return logging.WARN  # 30
    if(level == "error"):
        return logging.ERROR  # 40


"""
  ## Parameters
   - level: 'info', 'warn', 'error'
   - raw_event: map containing the actual event
   - opts:{async:"T/F","publish":T/F,"log":T/f}
            async(default true) : T to publish to event bus
            publish:(default false):T to publish to event bus
            log(defatul true): T to publish to event bus

    -app_vsn: app version given by env var 
  ## Examples
      do_log("info", event, {},"1.11")
       "Success"
      do_log(level, raw_event, opts)
       "Error"
  """


def do_log(level, raw_event, opts, app_vsn):
    log = True
    if("log" not in opts):
        log = True
    else:
        log = opts["log"]

    asyncc = True
    if("async" not in opts):
        if os.environ['ASYNC'] == None:
            asyncc = True
        else:
            asyncc = os.environ['ASYNC']
    else:
        asyncc = opts["async"]

    publish = False
    if("publish" not in opts):
        publish = False
    else:
        publish = opts['publish']

    res = parse_event(level, raw_event, app_vsn)
    if(log):
        log_event(res)

    if (publish == True):
        if (asyncc == True):
            t1 = threading.Thread(target=publish_event, args=(res, asyncc))
            t1.start()
        else:
            errors = []
            publish_res = publish_event(res, asyncc)
            if(publish_res):
                errors = errors
            else:
                errors = errors + [publish_res]
            if (len(errors) == 0):
                return True
            else:
                logging.error("Failed Publishing To RabbitMQ")
    else:
        return True

        # if(asyycnn true):
        #     return


"""
   ## Parameters
   - level: 'info', 'warn', 'error'
   - raw_event: map containing the actual event
    -app_vsn: app version given by env var 
  ## Examples
       parse_event("info",event,{}."1.1") 
"""
# Parses the event into standard structure


def parse_event(level, raw_event, app_vsn):
    event_source = raw_event.get("event_source")
    app_vsn = raw_event.get("app_vsn")
    component = raw_event.get("component", os.environ.get('COMPONENT'))
    service = raw_event.get("service", os.environ.get('SERVICE'))
    event_value = raw_event.get("event_value", raw_event.get("event_name"))
    correlation_id = raw_event.get("correlation_id")
    ou_id = raw_event.get("ou_id")
    x_request_id = raw_event.get("x_request_id")
    reference_id = raw_event.get("reference_id")
    reference_type = raw_event.get("reference_type")
    event_type = getevent_type(level, raw_event)
    dt = datetime.datetime.now(timezone.utc)
    utcTime = dt.replace(tzinfo=timezone.utc)
    timestamp = raw_event.get("timestamp", utcTime)
    details = raw_event.get("details")
    service_category = raw_event.get(
        "service_category", os.environ.get('SERVICE_CATEGORY'))

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
    timestamp = format_time_stamp(e["timestamp"])
    message = f'{e["reference_id"]}: {e["service"]} -> {e["event_type"]} - {e["event_value"]}'

    event = {
        "app_vsn": e["app_vsn"],
        "eid": e["eid"],
        "timestamp": timestamp,
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
        "details": json.dumps(e["details"]),
        "log_version": e["log_version"],
        "message": message
    }

    logging.log(log_level_generator(e["level"]), event)
    # logging.log(40,event)


"""
  Takes map ; publishes event to event bus
  ## Examples
       publish_event(e) 
"""


def publish_event(e, asyncc):
    timestamp = format_time_stamp(e["timestamp"])
    event = {
        "app_vsn": e["app_vsn"],
        "eid": e["eid"],
        "timestamp": timestamp,
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

    publisher = Publisher.getInstance()
    try:
        publisher.publish_message(event, generate_routing_key(e))
        return True
    except Exception as e:
        if(asyncc == True):
            raise Exception("Publish error occured")
        return e


"""
  Takes map ; returns  routing key for event bus
  ## Examples
       generate_routing_key(e) False
      "routingKey"
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
  Takes level string eventMap map and  returns  string
  ## Examples
       getevent_type("error",{}) 
      "routingKey"
"""


def getevent_type(level, eventMap):
    if(level == "error"):
        return "Exception" if (eventMap["event_type"] is None) else eventMap["event_type"]
    if(level == "warn"):
        return "Warning" if (eventMap["event_type"] is None) else eventMap["event_type"]
    else:
        return eventMap["event_type"]


def format_time_stamp(date_time_obj, opts="utc"):
    if(opts == "local"):
        return date_time_obj.isoformat()
    if(opts == "utc"):
        utc = date_time_obj.isoformat()
        return utc
