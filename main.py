import json

from flask import Flask, jsonify
from flask import request

from py_translator import Translator

from google.cloud import pubsub_v1

config = {
  "PROJECT": "cloud-hackathon-team-hermes",
  "PUBSUB_TOPIC": "voelligwurst",
}

app = Flask(__name__)
translator = Translator()

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(config["PROJECT"],
                                  config["PUBSUB_TOPIC"])


@app.route("/translate", methods=["POST"])
def translate():
    payload = request.get_json()
    en_msg = payload["message"]

    print(en_msg)
    ru_msg = translator.translate(en_msg, dest='ru').text

    data = dict(tranlated_msg=ru_msg, **payload)

    response = json.dumps(data).encode('utf-8')
    publisher.publish(topic_path, data=response)
    return jsonify(request_id=payload["request_id"],
                   # msg=ru_msg
                   )

if __name__ == '__main__':
    app.run(host='0.0.0.0')