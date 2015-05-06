from flask import Flask, request
import requests
import logging
import os
import json
import base64


app = Flask("Mail2Couch")

# log to stderr
app.logger.setLevel(logging.WARNING)
app.logger.addHandler(logging.StreamHandler())

warn = app.logger.warning

def _couch_setup():
    config = {}
    if os.environ.get("COUCHDB_USER"):
        config["auth"] = (os.environ.get("COUCHDB_USER"), os.environ.get("COUCHDB_PASSWORD"))

    return (os.environ.get("COUCHDB_URL"), config)


# accepting mandrill inbound format:
# https://mandrill.zendesk.com/hc/en-us/articles/205583207-What-is-the-format-of-inbound-email-webhooks-

def _handle_mandrill_email(message):
    attachments, images = {}, {}

    try:
        attachments = message.pop("attachments")
    except KeyError:
        pass

    try:
        images = message.pop("images")
    except KeyError:
        pass

    db_url, config = _couch_setup()

    doc = requests.post(db_url,
                        headers={"Content-Type": 'application/json'},
                        data=json.dumps(dict(type='x-email-inbound', msg=message)),
                        **config).json()
    doc_id = doc["id"]
    doc_rev = doc["rev"]

    doc_url = db_url + "/" + doc_id

    for dic in (attachments, images):
        if not dic:
            # empty, who cares...
            continue

        for filename, content in dic.iteritems():
            raw = content['content']
            if content["base64"]:
                raw = base64.b64decode(content['content'])
            url = doc_url + "/" + filename + "?rev=" + doc_rev
            doc = requests.put(url,
                               data=raw,
                               headers={"Content-Type": content["type"]},
                               **config).json()
            doc_rev = doc['rev']

    return doc_id



@app.route('/incoming/mandrill/default', methods=["POST"])
def mandrill_incoming():
    events = request.form.get("mandrill_events")
    ids = []

    if not events:
        return

    events = json.loads(events)

    for event in events:
        if event["event"] != "inbound":
            warn("There is a problem in your setup: /incoming/mandrill received non inbound emails")
            continue

        try:
            ids.append(_handle_mandrill_email(event["msg"]))
        # except BounceError as exc:
        except Exception as exc:
            if app.debug:
                raise
            warn("Problem parsing email {}: {}({})".format(event, type(exc), exc))

    return "Docs saved as: {}".format(", ".join(ids))


url, config = _couch_setup()
if not url:
    raise ValueError("You need to set COUCHDB_URL in the environment!")

db_stats = requests.get(url, **config)
if db_stats.status_code != 200:
    raise ValueError("Connecting to Database failed")

payload = db_stats.json()
if not "db_name" in payload:
    raise ValueError("It appears you haven't given me the address to a couchdb database")


if __name__ == "__main__":
    app.debug = True
    app.run()