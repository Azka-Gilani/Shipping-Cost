#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")

    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    speech = zone +"trial"

    print("Response:")
    print(speech)
    facebook_message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": zone,
                        "image_url": "http://blogs-images.forbes.com/vanessagrout/files/2015/03/shutterstock_130356110.jpg",
                        "subtitle": speech,
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "www.aarzpk.com"+zone,
                                "title": "View Details"
                            }
                        ]
                    }
                ]
            }
        }
    }
    
    
    message= {
      "attachment": {
         "type": "template",
          "payload": {
               "template_type": "generic",
               "elements": [{
               "title": "rift",
               "subtitle": "Next-generation virtual reality",
               "item_url": "https://www.oculus.com/en-us/rift/",               
               "image_url": "http://messengerdemo.parseapp.com/img/rift.png",
                "buttons": [{
                "type": "web_url",
                "url": "https://www.oculus.com/en-us/rift/",
                "title": "Open Web URL"
            }, 
                    {
                "type": "postback",
                "title": "Call Postback",
                "payload": "Payload for first bubble",
            }],
          }, 
                   {
                "title": "touch",
                "subtitle": "Your Hands, Now in VR",
                "item_url": "https://www.oculus.com/en-us/touch/",               
                "image_url": "http://messengerdemo.parseapp.com/img/touch.png",
                "buttons": [{
                "type": "web_url",
                "url": "https://www.oculus.com/en-us/touch/",
                "title": "Open Web URL"
            },
                    {
                "type": "postback",
                "title": "Call Postback",
                "payload": "Payload for second bubble",
            }]
          }]
        }
      }
    }
    print(json.dumps(facebook_message))


    return {
        "speech": speech,
        "displayText": zone,
        "data": {"facebook": message},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
