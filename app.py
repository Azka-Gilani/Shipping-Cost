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
    zone = parameters.get("location")
    

    #cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    speech1= "AARz.pk"
    print("Response:")
    print(speech)
     facebook_message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": query.get('title'),
                        "image_url":"http://blogs-images.forbes.com/vanessagrout/files/2015/03/shutterstock_130356110.jpg",
                        "subtitle": speech1,
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "http://www.aarz.pk/search?purpose=Sell&postedby=homepage&property_type=&locAreaOrKeyword="+zone,
                                "title": "View Details"
                            }
                        ]
                    }
                ]
            }
        }
    }


    return {
        "speech": speech,
        "displayText": speech,
        "data": {"facebook": facebook_message},
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
