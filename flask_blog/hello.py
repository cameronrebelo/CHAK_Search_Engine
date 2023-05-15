from flask import Flask, jsonify, request
from urllib.request import urlopen
import json
from flask import Flask, jsonify, request, render_template
from urllib.request import urlopen
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('solr.html')

@app.route('/query')
def get_solr_data():
    query_param = request.args.get('query')
    solr_url = 'http://localhost:8983/solr/rice_and_friends/select?q=title%3A'
    if query_param:
        solr_url += f'+{query_param}'  # Append the query parameter to the Solr URL
    solr_url += '*&wt=json'
    print(solr_url)
    connection = urlopen(solr_url)
    response = json.load(connection)
    num_found = response['response']['numFound']
    documents = [document.get('title','')
                 for document in response['response']['docs']]
    result = {
        'query' : query_param,
        'num_found': num_found,
        'documents': documents
    }
    return jsonify(result)
