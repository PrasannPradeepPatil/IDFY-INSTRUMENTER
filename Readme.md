INSTALLING THIS MODULE IN A PROJECT
1.keep your directory where you want to install this module
2.pip3 install --upgrade setuptools
3.pip3 install --upgrade pip
4.python3 -m pip install -e  ../IDFYINSTRUMENTER/-->This command will create a folder called idfy-instrumenter.egg.info(name acc to setup file) 
                                                  which allows us to use the module in editable mode


USING THIS MODULE IN A PROJECT
Consider a django project with application "myapplication"


views.py
from django.shortcuts import render
from django.http import HttpResponse
from idfyInstrumenterr import info


def index(request):  
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
   

    title = "INFO LOGGED"
    return HttpResponse("<h1>%s</h1>" % title)








