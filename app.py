from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    user = request.form.get('user_name')
    text = request.form.get('text') or ''
    err_msg = "You seem to have typed a badly formed command ('{}'). Usage options:\n/crux addcell [cell name]\n/crux addarticle [article url] [cell name]".format(text)
    if text is None or user is None:
        ret = err_msg
    else:
        tokens = text.split()
        ret = "Hello {}!\n".format(user)
        if len(tokens) < 2:
            ret += err_msg
        else:
            command = tokens[0]
            argument = ' '.join(tokens[1:])
            if command == 'addcell':
                if argument == 'Existing Cell':
                    ret += "Error: cell '{}' exists".format(argument)
                else:
                    ret += "Added new cell '{}'".format(argument)
            elif command == 'addarticle':
                cmdtokens = argument.split()
                if len(cmdtokens) < 2:
                    ret += err_msg
                else:
                    url = cmdtokens[0]
                    cell_name = ' '.join(cmdtokens[1:])
                    ret += "Added article from URL {} to cell '{}'".format(url, cell_name)
            else:
                ret += err_msg

    return {
        # "text": "Hello from Talybot! You are user {} in channel {} and you just said '{}'.".format(request.form.get('user_name'), request.form.get('channel_name'), request.form.get('text')),
        "text": ret,
        "response_type": "in_channel"
    }
