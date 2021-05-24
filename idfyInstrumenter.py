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
def log(level, raw_event, opts= []):
    if(level in levels):
        print(level, raw_event, opts, dir())


"""
  Info log
"""
def info(raw_event, opts=[]):
    print("info", raw_event, opts, dir())


"""
  Warning log
"""
def warn(raw_event, opts=[]):
    print("warn", raw_event, opts, dir())


"""
  Error log
"""
def error(raw_event, opts=[]):
    print("error", raw_event, opts, dir())
