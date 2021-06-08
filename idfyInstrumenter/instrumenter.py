import os
from datetime import timezone
import datetime
from .utils import makeRoutingKeySafe, eventSourceRoutingKey, uuid4
from .eventPublisher import PublishMessage
import threading



logLlevelMap = {
    "info": "Info",
    "warn": "Warning",
    "error": "Error"
}


def publishStatus(res):
    publishRes = publishEvent(res)
    if(publishRes == "PunlishedToRabbitMQ"):
        print("Published To Rabbit MQ")
    else:
        print("Error Publishing to RabbitMQ")


def errorStatus(res):
    errors = []
    publishRes = publishEvent(res)
    if(publishRes == "PunlishedToRabbitMQ"):
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
   - rawEvent: map containing the actual event
   - opts:{async:"T/F","publish":T/F,"log":T/f}
            async(default true) : T to publish to event bus
            publish:(default false):T to publish to event bus
            log(defatul true): T to publish to event bus
    
    -l : l is a map with following keys
         {"app","file","line","m","f","a"}
    -appVsn: app version given by env var 
  ## Examples

      doLog("info", event, {}, {},"1.11")
       "Success"

      doLog(level, rawEvent, opts, l)
       "Error"

  """


def doLog(level, rawEvent, opts, l, appVsn):
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

    res = parseEvent(level, rawEvent, l, appVsn)
    if(log):
        print("RESULT LOGGED TO CONSOLE")
        logEvent(res)

    if (publish == True):
        if (asyncc == True):
            t1 = threading.Thread(target=publishStatus, args=(res,))
            t1.start()
            t1.join()
            # publishStatus(res)

        else:
            errorStatus(res)
    else:
        print("Sucsss")


"""
   ## Parameters
   - level: 'info', 'warn', 'error'
   - rawEvent: map containing the actual event
    -l : l is a map with following keys
         {"app","file","line","m","f","a"}
    -appVsn: app version given by env var 
  ## Examples
       parseEvent("info",event,{}."1.1") 
"""
# Parses the event into standard structure


def parseEvent(level, rawEvent, l, appVsn): 
    eventSource = rawEvent["eventSource"] if(
        "eventSource" in rawEvent) else f'({l["app"]}) {l["file"]}: {l["line"]}: {l["m"]}.{l["f"]}/{l["a"]}'

    appVsn = rawEvent["appVsn"] if("appVsn" in rawEvent) else appVsn
    component = rawEvent["component"] if(
        "component" in rawEvent) else os.environ['component']
    service = rawEvent["service"] if(
        "service" in rawEvent) else os.environ['service']
    eventValue = rawEvent["eventValue"] if(
        "eventValue" in rawEvent) else rawEvent["eventName"]
    correlationId = rawEvent["correlationId"] if(
        "correlationId" in rawEvent) else "correlationId"  # logger_metadata[:correlationId]
    ouId = rawEvent["ouId"] if(
        "ouId" in rawEvent) else "ouId"   # logger_metadata[:ouId]
    xRequestId = rawEvent["xRequestId"] if(
        "xRequestId" in rawEvent) else "xRequestId"  # logger_metadata[:xRequestId]

    referenceId = rawEvent["referenceId"] if("referenceId" in rawEvent) else "referenceId"     # logger_metadata[:referenceId]
    referenceType = rawEvent["referenceType"] if(
        "referenceType" in rawEvent) else "referenceType"    # logger_metadata[:referenceType]
    eventType = getEventType(level, rawEvent)
    dt = datetime.datetime.now(timezone.utc)
    utcTime = dt.replace(tzinfo=timezone.utc)
    timestamp = rawEvent["timestamp"] if(
        "timestamp" in rawEvent) else utcTime
    details = rawEvent["details"] if(
        type(rawEvent["details"]) is dict) else dict({})
    serviceCategory = rawEvent["serviceCategory"] if(
        "serviceCategory" in rawEvent) else os.environ('serviceCategory')

    return {
        "appVsn": appVsn,
        "eid": uuid4(),
        "component": component,
        "service": service,
        "eventValue": eventValue,
        "correlationId": correlationId,
        "ouId": ouId,
        "xRequestId": xRequestId,
        "timestamp": timestamp,
        "details": details,
        "referenceId": referenceId,
        "referenceType": referenceType,
        "eventType": eventType,
        "level": level,
        "levelValue": logLlevelMap[level],
        "serviceCategory": serviceCategory,
        "eventSource": eventSource,
        "logVersion": rawEvent["logVersion"]
    }


"""
  Takes map ; publishes event to console

  ## Examples
       publishEvent(e) 
"""


def logEvent(e):
    # timestamp = IdfyInstrumenter.format_timestamp(e[timestamp, :log) 
    message = f'{e["referenceId"]}: {e["service"]} -> {e["eventType"]} - {e["eventValue"]}'

    event = {
        "appVsn": e["appVsn"],
        "eid": e["eid"],
        #   "timestamp" : timestamp,
        "xRequestId": e["xRequestId"],
        "eventSource": e["eventSource"],
        "logLlevel": e["levelValue"],
        "serviceCategory": e["serviceCategory"],
        "ouId": e["ouId"],
        "correlationId": e["correlationId"],
        "referenceId": e["referenceId"],
        "referenceType": e["referenceType"],
        "component": e["component"],
        "service": e["service"],
        "eventType": e["eventType"],
        "eventName": e["eventValue"],
        #   "details" : Jason.encode!(e[details),
        "logVersion": e["logVersion"],
        "message": message
    }

   # Logger.log(e.level, fn -> {"", event} end)
    print(event)


"""
  Takes map ; publishes event to event bus

  ## Examples
       publishEvent(e) 
"""

publishMessage = PublishMessage()


def publishEvent(e):
    # timestamp = IdfyInstrumenter.format_timestamp(e[timestamp, :publish) 
    event = {
        "appVsn": e["appVsn"],
        "eid": e["eid"],
        # "timestamp" : timestamp,
        "xRequestId": e["xRequestId"],
        "eventSource": e["eventSource"],
        "logLlevel": e["levelValue"],
        "serviceCategory": e["serviceCategory"],
        "ouId": e["ouId"],
        "correlationId": e["correlationId"],
        "referenceId": e["referenceId"],
        "referenceType": e["referenceType"],
        "component": e["component"],
        "service": e["service"],
        "eventType": e["eventType"],
        "eventValue": e["eventValue"],
        "logVersion": e["logVersion"],
        "details": e["details"]
    }

    try:
        while(True):
            publishMessage.publishMessage(event, generateRoutingKey(e))
        return "PunlishedToRabbitMQ"
    except Exception as e:
        return e


"""
  Takes map ; returns  routing key for event bus

  ## Examples

       generateRoutingKey(e) False
      "routingKey"
"""


def generateRoutingKey(e):
    eventSource = makeRoutingKeySafe(
        eventSourceRoutingKey(e["eventSource"]))
    serviceCategory = makeRoutingKeySafe(e["serviceCategory"])
    component = makeRoutingKeySafe(e["component"])
    service = makeRoutingKeySafe(e["service"])
    eventType = makeRoutingKeySafe(e["eventType"])
    logVersion = makeRoutingKeySafe(e["logVersion"])

    return f'{e["levelValue"]}.{eventSource}.{logVersion}.{serviceCategory}.{component}.{service}.{eventType}'


"""
  Takes level string eventMap map and  returns  string

  ## Examples

       getEventType("error",{}) 
      "routingKey"

"""


def getEventType(level, eventMap):
    if(level == "error"):
        return "Exception" if (eventMap["eventType"] is None) else eventMap["eventType"]
    if(level == "warn"):
        return "Warning" if (eventMap["eventType"] is None) else eventMap["eventType"]
    else:
        return eventMap["eventType"]



def formatTimeStamp(opts):
    if(opts == "local"):
        local     = datetime.datetime.now()
        return local
    if(opts == "utc"):
        utc       = datetime.datetime.utcnow()
        return utc
    if(opts == "isoLocal"):
        isoLocal = datetime.datetime.now().isoformat() 
        return isoLocal
    if(opts == "isoUtc"):
        isoUtc   = datetime.datetime.utcnow().isoformat() 
        return isoUtc




