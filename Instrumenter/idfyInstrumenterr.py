from .idfyInstrumenter import instrumenter

"""
  Log function that takes level as argument

  ## Parameters
   - level: 'info', 'warn', 'error'
   - raw_event: map containing the actual event
   - opts:
     - log (bool): Log to stdout (default `true`)
     - publish (bool): Publish log to event bus (default `false`)

  ## Examples

      log(level, raw_event, opts)
      "Success"

      log(level, raw_event, opts)
      [log: "Some error", publish: "Some error"]

"""
levels = ["info","warn","error"]
# Get application & file name
def logger(level, raw_event, opts, l,app_vsn):
  instrumenter.do_log(level, raw_event, opts, l, app_vsn)


def log(level, raw_event, opts, l,app_vsn):
    if(level in levels):
        logger(level, raw_event, opts, l,app_vsn)


"""
  Info log
"""
def info(level, raw_event, opts, l,app_vsn):
    logger(level, raw_event, opts, l,app_vsn)
    


"""
  Warning log
"""
def warn(level, raw_event, opts, l,app_vsn):
    logger(level, raw_event, opts, l,app_vsn)


"""
  Error log
"""
def error(level, raw_event, opts, l,app_vsn):
    logger(level, raw_event, opts, l,app_vsn)



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

opts = {"async":True,"publish":True,"log":True}


info("info",e,opts,{},"1.11")

