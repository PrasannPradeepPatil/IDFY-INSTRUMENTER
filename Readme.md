INSTALLING THIS MODULE IN A PROJECT
1.keep your directory where you want to install this module
2.pip3 install --upgrade setuptools
3.pip3 install --upgrade pip
4.python3 -m pip install -e  ../IDFYINSTRUMENTER/     -->This command will create a folder called idfyinstrumenter.egg.info 
                                                         which allows us to use the module in editable mode


USING THIS MODULE IN A PROJECT
Consider a django project with application "myapplication"


views.py
from django.shortcuts import render
from django.http import HttpResponse
from idfyInstrumenterr import info


def index(request):
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
   

    title = "INFO LOGGED"
    return HttpResponse("<h1>%s</h1>" % title)








