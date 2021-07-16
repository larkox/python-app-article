from bottle import route, run, post, static_file, request
from model import Binding, Call, CallResponse, Form, Encoder
import requests
import json

@route('/manifest')
def manifest():
    return static_file("manifest.json", "./")

@route('/static/icon.png')
def icon():
    return static_file("icon.png", "./")

@post('/bindings')
def bindings():
    pingCommand = Binding()
    pingCommand.location = "ping"
    pingCommand.label = "ping"
    pingCommand.call = Call()
    pingCommand.call.path = "/command/ping"
    pingCommand.form = Form()
    pingCommand.icon = "icon.png"
    
    baseCommandBinding = Binding()
    baseCommandBinding.label = "blogapp"
    baseCommandBinding.description = "Commands for Blog App"
    baseCommandBinding.location = "blogapp"
    baseCommandBinding.bindings = []
    baseCommandBinding.bindings.append(pingCommand)

    commandBinding = Binding()
    commandBinding.location = "/command"
    commandBinding.bindings = []
    commandBinding.bindings.append(baseCommandBinding)

    channelHeaderBinding = Binding()
    channelHeaderBinding.location = "/channel_header"
    channelHeaderBinding.bindings = []
    channelHeaderBinding.bindings.append(pingCommand)

    appBindings = []
    appBindings.append(commandBinding)
    appBindings.append(channelHeaderBinding)

    callResponse = CallResponse()
    callResponse.type = "ok"
    callResponse.data = appBindings
    return Encoder().encode(callResponse)

@post('/command/ping/<type>')
def ping(type):
    callResponse = CallResponse()
    callResponse.type = "ok"
    callResponse.markdown = "PONG!"
    print(request.json)
    return Encoder().encode(callResponse)

run(host='localhost', port=3030, debug=True)
