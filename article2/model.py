from json import JSONEncoder

class Expand:
    app = ""
    acting_user = ""
    acting_user_access_token = ""
    admin_access_token = ""
    channel = ""
    mentioned = ""
    post = ""
    root_post = ""
    team = ""
    user = ""
    oauth2_app = ""
    oauth2_user = ""

class Call:
    path = ""
    expand = Expand()
    state = ""

class SelectOption:
    label = ""
    value = ""
    icon_data = ""

class Field:
    name = ""
    type = ""
    is_required = False
    readonly = False
    value = ""
    description = ""
    label = ""
    hint = ""
    position = 0
    modal_label = ""
    multiselect = False
    refresh = False
    options = []
    subtype = ""
    min_length = 0
    max_length = 0

class Form:
    title = ""
    header = ""
    footer = ""
    icon = ""
    call = Call()
    submit_buttons = ""
    cancel_button = False
    submit_on_cancel = False
    fields = []

class Binding:
    location = ""
    icon = ""
    label = ""
    hint = ""
    description = ""
    role_id = ""
    depends_on_team = ""
    depends_on_channel = ""
    depends_on_user = ""
    depends_on_post = ""
    call = Call()
    bindings = []
    form = Form()


class CallResponse:
    type = ""
    markdown = ""
    data = ""
    error = ""
    navigate_to_url = ""
    use_external_browser = False
    call = Call()
    form = Form()

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
