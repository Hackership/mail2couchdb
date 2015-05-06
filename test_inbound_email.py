# -*- coding: utf-8 -*-
import urllib2
import urllib

import random
import json
import base64

FROM = "asd0.782931682522@gmail.com"

DATA = {
    "attachments": {
        "equal.jpg": {
            "content": "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",
            "name": "equal.jpg",
            "base64": True,
            "type": "image/jpeg"
        },
        "hackership.txt": {
            "content": """
...........................................................................................
.........##..##...####....####...##..##..######..#####....####...##..##..######..#####.....
.........##..##..##..##..##..##..##.##...##......##..##..##......##..##....##....##..##....
.........######..######..##......####....####....#####....####...######....##....#####.....
.........##..##..##..##..##..##..##.##...##......##..##......##..##..##....##....##........
.........##..##..##..##...####...##..##..######..##..##...####...##..##..######..##........
...........................................................................................
""",
            "name": "hackership.txt",
            "base64": False,
            "type": "plain/text"
        }
    },
    "images" : {
        "hackership.png": {
            "content": """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""",
            "name": "hackership.png",
            "base64": True,
            "type": "image/png"
        }
    },
    "cc": [
        ["bob@example.com", "Bob Johnson"]
    ],
    "dkim": {
        "signed": False,
        "valid": False
    },
    "email": "testing+123testing@example.com",
    "from_email": "john@example.com",
    "from_name": "John Smith",
    "headers": {
        "Cc": "Bob Johnson <bob@example.com>",
        "Content-Type": "multipart/mixed; boundary=\"51643cec_66ef438d_d22c\"",
        "Date": "Tue, 9 Apr 2013 12:08:12 -0400",
        "From": "John Smith <john@example.com>",
        "Message-Id": "<54C9A31C34DF40409355EC9BB763EF15@example.com>",
        "Mime-Version": "1.0",
        "Received": ["from mail-gh0-f179.google.com (mail-gh0-f179.google.com [209.85.160.179]) by ip-10-254-10-35 (Postfix) with ESMTPS id 255244B40C5 for <testing+123testing@example.com>; Tue, 9 Apr 2013 16:08:20 +0000 (UTC)", "by mail-gh0-f179.google.com with SMTP id z12so1085045ghb.10 for <testing+123testing@example.com>; Tue, 09 Apr 2013 09:08:19 -0700 (PDT)", "from [10.0.0.83] (65-23-202-215.prtc.net. [65.23.202.215]) by mx.google.com with ESMTPS id s45sm43951018yhk.22.2013.04.09.09.08.15 (version=TLSv1 cipher=RC4-SHA bits=128/128); Tue, 09 Apr 2013 09:08:17 -0700 (PDT)"],
        "Subject": "Testing",
        "To": "Testing Staging <testing+123testing@example.com>",
        "X-Gm-Message-State": "",
        "X-Google-Dkim-Signature": "",
        "X-Mailer": "sparrow 1.6.4 (build 1178)",
        "X-Received": "by 10.236.209.67 with SMTP id r43mr16105835yho.197.1365523699219; Tue, 09 Apr 2013 09:08:19 -0700 (PDT)"
    },
    "html": "<p>We no speak americano</p>",
    "raw_msg": "",
    "sender": None,
    "spam_report": {
        "matched_rules": [{
                "description": "RBL: Sender listed at http://www.dnswl.org/, low",
                "name": "RCVD_IN_DNSWL_LOW",
                "score": -0.7
            }, {
                "description": None,
                "name": None,
                "score": 0
            }, {
                "description": "in list.dnswl.org]",
                "name": "listed",
                "score": 0
            }, {
                "description": "Local part of To: address appears in Subject",
                "name": "LOCALPART_IN_SUBJECT",
                "score": 0.7
            }, {
                "description": "BODY: HTML included in message",
                "name": "HTML_MESSAGE",
                "score": 0
            }
        ],
        "score": 0
    },
    "spf": {
        "detail": "sender SPF authorized",
        "result": "pass"
    },
    "subject": "Testing",
    "tags": [],
    "text": "\nThis is awesome!\n\n",
    "to": [
        ["testing+123testing@example.com", "Testing Staging"]
    ]
}

ENDPOINT = "http://localhost:5000/incoming/mandrill/default"


def run(**updates):
    DATA.update(updates)
    postData = {"mandrill_events":json.dumps([{
        "event": "inbound",
        "ts": 1365523701,
        "msg": DATA}])}
    print(urllib2.urlopen(ENDPOINT, urllib.urlencode(postData)).read())

if __name__ == "__main__":
    run()
