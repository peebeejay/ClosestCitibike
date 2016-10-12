from flask import Flask, render_template, jsonify, request
import Citibike
import logging, sys, os
import googlemaps

app = Flask(__name__)
Citibike.main()


@app.route('/')
def citibike():
    return render_template('citibike.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route("/receive_coord")
def receive_coord():
    a_lat = request.args.get('lat', 0, type=float)
    a_lon = request.args.get('lon', 0, type=float)

    final = Citibike.processCoords(a_lat, a_lon, stationReq_=5, partySize_=1)
    print(Citibike.ChatbotStations(final, "TEST"))

    return jsonify(result=final)


@app.route('/chatbot', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "You have reached the URL for chatbot requests. You will find nothing else to do here.", 200


@app.route('/chatbot', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Data: ", data)

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                messages = Citibike.processMessage(messaging_event)

                for message in messages:
                    Citibike.sendMessage(sender_id, message)

    return "ok", 200


if __name__ == "__main__":
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    app.run()
