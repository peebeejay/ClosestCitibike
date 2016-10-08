from flask import Flask, render_template, jsonify, request
from Citibike import APICall, process_list, create_final_list
import logging, sys, os, json, requests


app = Flask(__name__)


@app.route('/')
def citibike():
    return render_template('citibike.html')


@app.route("/receive_coord")
def receive_coord():
    a_lat = request.args.get('lat', 0, type=float)
    a_lon = request.args.get('lon', 0, type=float)
    print("Coordinates:", a_lat, ", ", a_lon)
    partySize = 1
    stationReq = 5

    # Call the Citibike API and get the latest station data
    station_information = CitibikeAPICaller.getStationInfo()[0]
    station_status = CitibikeAPICaller.getStationStatus()[0]
    print("---> Data is Fresh as of: ", str(CitibikeAPICaller.getStationStatus()[1]))

    # Process data received from Citibike API
    station_data_list = process_list(station_status, station_information, a_lat, a_lon)
    final = create_final_list(station_data_list, pSize=partySize, statReq=stationReq)
    return jsonify(result=final)


@app.route('/chatbot', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "You have reached the URL for chatbot requests. You will find nothing else to do here.", 200


@app.route('/chatbot', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    log(data["entry"][0]["messaging"][0]["message"].keys())
    log(data["entry"][0]["messaging"][0]["message"])
    
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                log("**********")
                if "text" in messaging_event["message"].keys():
                    log("--> TEXT MESSAGE <--")
                elif "attachments" in messaging_event["message"].keys():
                    log("--> LIKELY MAP MESSAGE <--")
                    if "payload" in messaging_event["message"]["attachments"][0].keys():
                        log("LATITUDE: " + str(messaging_event["message"]["attachments"][0]["payload"]["coordinates"]["lat"]))
                        log("LONGITUDE: " + str(messaging_event["message"]["attachments"][0]["payload"]["coordinates"]["long"]))
                        # copy code from receive_coords here



    '''
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    send_message(sender_id, "got it, thanks!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
                    '''
    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()




CitibikeAPICaller = APICall(interval=30)

if __name__ == "__main__":
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    app.run()
