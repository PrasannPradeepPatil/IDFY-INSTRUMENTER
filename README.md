
# IdfyInstrumenter

Used for structured logging in stdout & publishing events to event bus



## Installing this module in a project 

1.keep your directory where you want to install this module
2.pip3 install --upgrade setuptools
3.pip3 install --upgrade pip
4.python3 -m pip install -e  ../IDFYINSTRUMENTER/-->This command will create a folder called idfy-instrumenter.egg.info(name acc to setup file) 
                                                    which allows us to use the module in editable mode




## Configuration

| Key                   | Type          | Default                             | Description                       |
|-----------------------|---------------|-------------------------------------|-----------------------------------|
|service_category       |string         |Required                             |Default Service Category           |
|amqp_url               |string         |Required                             |RabbitMQ publish URL               |
|component              |string         |`nil`                                |Default Component                  |
|service                |string         |`nil`                                |Default Service                    |
|async                  |bool           |`true`                               |Publish logs in a new process      |
|publish_enabled        |bool/string    |`true`                               |Enable/Disable publish to event bus|
|exchange               |string         |idfy-instrumenter                    |Configure RMQ Exchange             |
|publisher              |String         |event_publisher                      |Configure custom RMQ publisher     |



### Fields

* correlation_id
* x_request_id
* ou_id
* reference_id
* reference_type

## Usage

```python
    from idfy_instrumenter import info
  
    def i_need_some_instrumentation:
        e = {
            "app_vsn": "app_vsn",
            "eid": "eid",
            "timestamp": "timestamp",
            "x_equest_id": "x_equest_id",
            "event_source": "event_source",
            "logLevel": "level_value",
            "service_category": "service_category",
            "ou_id": "ou_id",
            "correlation_id": "correlation_id",
            "referenceI_id": "referenceI_id",
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
   

```

### Functions

```python
    info(event_map, opts)
    warn(event_map, opts)
    error(event_map, opts)

```

#### Optional arguments
* `:log`: (Default: `true`) Log to stdout?
* `:publish`: (Default: `false`) Publish to event bus?
* `:async`: (Default: `true`) Publish log in a new process

## Custom Publisher

You can implement your own custom rmq publisher & pass it to the library







