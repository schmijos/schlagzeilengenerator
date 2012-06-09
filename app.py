import os
from random import randrange

from flask import Flask
from flask_heroku import Heroku
from pymongo import Connection


app = Flask(__name__)
heroku = Heroku(app)

connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
db = connection[app.config['MONGODB_DB']]
db.authenticate(app.config['MONGODB_USER'], app.config['MONGODB_PASSWORD'])


### Helper functions ###

def mongo_get_random(collection_name):
    collection = db[collection_name]
    count = collection.count()
    offset = randrange(1, count)
    return collection.find().skip(offset).limit(1)[0]

def generate_headline():
    """Generate and return an awesome headline."""

    # Correct endings
    adjective_endings = {
        'm': 'r',
        'w': '',
        's': 's',
        'p': '',
    }

    # Get random database entries
    d_intro = mongo_get_random('intro')
    d_adjective = mongo_get_random('adjective')
    d_prefix = mongo_get_random('prefix')
    d_suffix = mongo_get_random('suffix')
    d_action = mongo_get_random('action')

    # Get data from mongo dictionaries
    case = d_suffix['case']
    intro = d_intro['text']
    adjective = d_adjective['text'] + adjective_endings[case]
    prefix = d_prefix['text']
    suffix = d_suffix['text']
    if case == 'p':
        action = '%s %s' % (d_action['action_p'], d_action['text'])
    else:
        action = '%s %s' % (d_action['action_s'], d_action['text'])

    return '%s: %s %s-%s %s!' % (intro, adjective, prefix, suffix, action)


### Views ###

@app.route('/')
def headline():
    return generate_headline()


### Dev Server ###

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG') in ['true', 'True', 'TRUE', 't', 'T', '1']
    app.run(host='0.0.0.0', port=port, debug=debug)
