from flask import Flask, request, redirect
import os
import sys
import logging

SLACK_AUTHORIZE_URL = 'https://slack.com/oauth/authorize'
SLACK_ACCESS_URL = 'https://slack.com/api/oauth.access'
SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

@app.route("/", methods=['GET', 'POST'])
def index():
    user_name = request.form.get('user_name') or ''
    text = request.form.get('text') or ''
    scope = request.form.get('scope')
    code = request.form.get('code')
    team = request.form.get('team')
    error = request.form.get('error')
    print("user_name='{}', text='{}' scope='{}' state='{}' team='{}' code='{}' error='{}'".format(
        user_name, text, scope, request.form.get('state'), team, code, error
        ))

    # Initial implementation of Slack's OAuth 2.0 requirements
    # if code is None:
    #     auth_redirect_url = "{}?client_id={}&scope={}&team={}".format(SLACK_AUTHORIZE_URL, SLACK_CLIENT_ID, scope, team)
    #     redirect(auth_redirect_url, code=302)
    # else:
    #     access_url = "{}?client_id={}&client_secret={}&code={}".format(SLACK_ACCESS_URL, SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, code)
    #     # TODO access URL to get and keep token for use in APIs


    return parse_message(user_name, text)

def parse_message(user_name, text):
    cap_user_name = user_name.title()
    err_msg = "You seem to have typed a badly formed command ('{}'). Usage options:\n/crux addcell [cell name]\n/crux addarticle [article url] [cell name]".format(text)
    response_type = 'ephemeral'
    ret = ''
    if text is None or user_name is None:
        ret = err_msg
    else:
        tokens = text.split()
        if len(tokens) < 2:
            ret = err_msg
        else:
            command = tokens[0]
            argument = ' '.join(tokens[1:])
            if command == 'addcell':
                if argument == 'Existing Cell':
                    ret = "Error: cell '{}' exists".format(argument)
                else:
                    ret = "{} has added new cell '{}'".format(cap_user_name, argument)
                    response_type = 'in_channel'
            elif command == 'addarticle':
                cmdtokens = argument.split()
                if len(cmdtokens) < 2:
                    ret = err_msg
                else:
                    url = cmdtokens[0]
                    cell_name = ' '.join(cmdtokens[1:])
                    ret = "{} has added article from URL {} to cell '{}'".format(cap_user_name, url, cell_name)
                    response_type = 'in_channel'
            else:
                ret = err_msg

    return {
        "text": ret,
        "response_type": response_type
    }
