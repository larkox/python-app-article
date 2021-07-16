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

    pongCommand = Binding()
    pongCommand.location = "pong"
    pongCommand.label = "pong"
    pongCommand.call = Call()
    pongCommand.call.path = "/command/pong"
    pongCommand.form = Form()

    baseCommandBinding = Binding()
    baseCommandBinding.label = "blogapp"
    baseCommandBinding.description = "Commands for Blog App"
    baseCommandBinding.location = "blogapp"
    baseCommandBinding.bindings = []
    baseCommandBinding.bindings.append(pingCommand)
    baseCommandBinding.bindings.append(pongCommand)

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

@post('/command/pong/<type>')
def pong(type):
    callResponse = CallResponse()
    callResponse.type = "ok"

    mm_url = request.json["context"]["mattermost_site_url"]
    bot_token = request.json["context"]["bot_access_token"]
    user_id = request.json["context"]["acting_user_id"]
    bot_id = request.json["context"]["bot_user_id"]
    r = requests.post(mm_url + "/api/v4" + "/channels/direct", headers={"Authorization": "BEARER " + bot_token}, data=json.dumps([user_id, bot_id]))
    if r.status_code != 201:
        callResponse.type = "error"
        callResponse.error = "Cannot create direct channel with the bot. Status code = % s" % r.status_code
        return Encoder().encode(callResponse)
    channel_id = r.json()["id"]
    r = requests.post(mm_url + "/api/v4" + "/posts", headers={"Authorization": "BEARER " + bot_token}, json={
        "channel_id": channel_id,
        "message": "PING!",
    })
    if r.status_code != 201:
        callResponse.type = "error"
        callResponse.error = "Cannot post message. Status code = % s" % r.status_code
        return Encoder().encode(callResponse)

    return Encoder().encode(callResponse)

run(host='localhost', port=3030, debug=True)
