import json
from flask import Flask, jsonify, request, render_template, url_for, flash, redirect
from urllib.request import urlopen

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_input = request.form['search-input']
        if not search_input:
            flash('Title is required!')
        else:
            return redirect(url_for('index'))

    return render_template('solr.html')


@app.route('/query')
def get_solr_data():
    query_param = request.args.get('query')
    solr_url = 'http://localhost:8983/solr/rice_and_friends/select?q=title%3A'
    if query_param:
        # Append the query parameter to the Solr URL
        solr_url += f'+{query_param}'
    solr_url += '*&wt=json'
    print(solr_url)
    connection = urlopen(solr_url)
    response = json.load(connection)
    num_found = response['response']['numFound']
    documents = [document.get('title', '')
                 for document in response['response']['docs']]

    return render_template('results.html', documents=documents)


if __name__ == '__main__':
    app.run()
