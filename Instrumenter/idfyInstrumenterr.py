from .idfyInstrumenter import instrumenter

"""
  Log function that takes level as argument

  ## Parameters
   - level: 'info', 'warn', 'error'
   - rawEvent: map containing the actual event
   - opts:
     - log (bool): Log to stdout (default `true`)
     - publish (bool): Publish log to event bus (default `false`)

  ## Examples

      log(level, rawEvent, opts)
      "Success"

      log(level, rawEvent, opts)
      [log: "Some error", publish: "Some error"]

"""
levels = ["info","warn","error"]
# Get application & file name
def logger(level, rawEvent, opts, l,appVsn):
  instrumenter.doLog(level, rawEvent, opts, l, appVsn)


def log(level, rawEvent, opts, l,appVsn):
    if(level in levels):
        logger(level, rawEvent, opts, l,appVsn)


"""
  Info log
"""
def info(level, rawEvent, opts, l,appVsn):
    logger(level, rawEvent, opts, l,appVsn)
    


"""
  Warning log
"""
def warn(level, rawEvent, opts, l,appVsn):
    logger(level, rawEvent, opts, l,appVsn)


"""
  Error log
"""
def error(level, rawEvent, opts, l,appVsn):
    logger(level, rawEvent, opts, l,appVsn)



########################DRIVER CODE############################
e = {
    "appVsn": "appVsn",
    "eid": "eid",
    "timestamp": "timestamp",
    "xRequestId": "xRequestId",
    "eventSource": "eventSource",
    "logLevel": "levelValue",
    "serviceCategory": "serviceCategory",
    "ouId": "ouId",
    "correlationId": "correlationId",
    "referenceId": "referenceId",
    "referenceType": "referenceType",
    "component": "component",
    "service": "service",
    "eventType": "eventType",
    "eventValue": "eventValue",
    "logVersion": "logVersion",
    "details": "details",
    "levelValue": "levelValue"

}

opts = {"async":True,"publish":True,"log":True}


info("info",e,opts,{},"1.11")



