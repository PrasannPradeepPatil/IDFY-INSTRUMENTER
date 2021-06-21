from idfyinstrumenter import instrumenter

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
def logger(level, raw_event, opts,app_vsn):
  instrumenter.do_log(level, raw_event, opts, app_vsn)


def log(level, raw_event, opts,app_vsn):
    if(level in levels):
        logger(level, raw_event, opts,app_vsn)


"""
  Info log
"""
def info(level, raw_event, opts,app_vsn):
    logger(level, raw_event, opts,app_vsn)
    


"""
  Warning log
"""
def warn(level, raw_event, opts,app_vsn):
    logger(level, raw_event, opts,app_vsn)


"""
  Error log
"""
def error(level, raw_event, opts,app_vsn):
    logger(level, raw_event, opts,app_vsn)


