import flask
from flask import Flask, request, jsonify
import pandas as pd
from JsonParser import JsonParser
from TitleHandler import TitleHandler
from UrlParser import UrlParser
from DecisionTreeModel import DecisionTreeModel

app = Flask(__name__)
app.config["DEBUG"] = True

def encodeFields(df):
    # return dict with 'raw_url', 'raw_title', & 'tweet_ids'
    data = JsonParser(df).execute()
    
    # encode each of the data_portions
    encodeUrl = UrlParser(data['raw_url']).execute()
    encodeTitle = TitleHandler(data['raw_title']).execute()
    encodedTweet_ids = data['tweet_ids']

    newDF = pd.DataFrame()
    newDF['domain_type'] = [encodeUrl['domain_type']]
    newDF['protocol'] = [encodeUrl['protocol']]
    newDF["title_capital_freq"] = [encodeTitle['title_capital_freq']]
    newDF["tweet_ids"] = [encodedTweet_ids]
    newDF["internal_links"] = [encodeUrl['internal_links']]

    #print("\n\n--------------------\n",newDF , "\n--------------------\n\n")
    return newDF

@app.route('/api/v1/webApp', methods=['POST'])
def webApp():
    contentDict = request.get_json() # Creates dictionary from json we send
    if contentDict == None:
        return {"response": "400 Bad Request"}
    # call class which returns confidence score...
    # modify, thenreturn new json
    # loaded_json = json.loads(json_data)
    df = pd.DataFrame.from_dict(contentDict)

    # encode and return dataframe
    y_final = encodeFields(df)

    y_pred, accuracy = DecisionTreeModel(y_final).execute()

    print("For the link you provided the model determined it is...DRUM ROLL PLEASE...\n")
    if(y_pred == 0):
        print("IT IS THE TRUTH, REAL NEWS!!!!\n")
    else:
        print("IT IS FAKE NEWS!!!\n")
    
    '''
    https://fakenewsurldetector.herokuapp.com/ for webApp json attributes (just the url info)
    https://github.com/Adatrader/FakeNewsDetector/blob/main/facebookResponse.json for facebook json attributes being sent
    https://github.com/Adatrader/FakeNewsDetector/blob/main/twitterResponse.json for twitter json attributes being sent
    
    Example accessing data:
    url = content['url']
    origin = contentDict['origin']
    '''

    # TODO: Call your functions here to update 'confidence_score' in dictionary and then return
    contentDict['confidence_score'] = accuracy
    contentDict['isReal'] = 1 if (y_pred == 0) else 0
    return jsonify(contentDict)

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

'''
Deploying your project on Heroku:
https://stackabuse.com/deploying-a-flask-application-to-heroku/
Follow the heroku section halfway down the page

Heroku needs:
Procfile (included - no modification required)
requirements.txt (add to it the dependencies you're using)
runtime.txt (included - no modification required unless not using python 3.8.6)
and your app.py
'''
