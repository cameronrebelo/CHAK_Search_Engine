from flask import Flask, jsonify
from urllib.request import urlopen
import json

app = Flask(__name__)


@app.route('/')
def get_solr_data():
    connection = urlopen(
        'http://localhost:8983/solr/rice_and_friends/select?q=*:*&wt=json')
    response = json.load(connection)
    num_found = response['response']['numFound']
    documents = [document['title']
                 for document in response['response']['docs']]
    result = {
        'num_found': num_found,
        'documents': documents
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run()
