import re

class JsonParser:
    def __init__(self, jsonDataFrame):
        self.data = {}
        self.json = jsonDataFrame

    def execute(self):
        self.data['raw_url'] = self.jsonExtractUrl(self.json)
        self.data['raw_title'] = self.jsonExtractTitle(self.json)
        self.data['tweet_ids'] = self.jsonExtractTweetIds(self.json)
        return self.data

    def jsonExtractUrl(self, jsonDataFrame):
        url = ""
        try:
            for col_names in jsonDataFrame:
                if col_names == "entities":
                    if 'expanded_url' in jsonDataFrame[col_names]['urls'][0]:
                        url = jsonDataFrame[col_names]['urls'][0]['expanded_url']
                    elif 'url' in jsonDataFrame[col_names]['urls'][0]:
                        url = jsonDataFrame[col_names]['urls'][0]['url']
        except Exception:
            # expanded url not found !
            url = None
        # if empty
        if(url == ""):
            url = None
        return url


    def jsonExtractTitle(self, jsonDataFrame):
        regexUrl = re.compile(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
        title = ""
        try:
            for col_names in jsonDataFrame:
                if col_names == "text":
                    if 'entities' in jsonDataFrame[col_names]:
                        title = jsonDataFrame[col_names]['entities']
                    elif 'description' in jsonDataFrame[col_names]:
                        title = jsonDataFrame[col_names]['description']
                    elif 'name' in jsonDataFrame[col_names]:
                        title = jsonDataFrame[col_names]['name']
        except Exception:
            # no title found!
            title = ""
        
        if( not isinstance(title, str)):
            title = "" # not valid therefore make string

        # remove any embedded links
        if(title != ""):
            parts = title.split(" ")
            newStr = ""
            for word in parts:
                if not regexUrl.match(word):
                    newStr += word + " "

            title = newStr
        
        return title


    def jsonExtractTweetIds(self, jsonDataFrame):
        tweets = 0
        for col_names in jsonDataFrame:
            try:
                # add quote count
                if col_names == "quote_count":
                    if 'id' in jsonDataFrame[col_names]:
                        tweets += jsonDataFrame[col_names]['id']
                # add reply count
                if col_names == 'reply_count':
                    if 'favourites_count' in jsonDataFrame[col_names]:
                        tweets += jsonDataFrame[col_names]['favourites_count']
                    elif 'favorites_count' in jsonDataFrame[col_names]:
                        tweets += jsonDataFrame[col_names]['favorites_count']
                # add retweet count
                if col_names == 'retweet_count':
                    if 'id' in jsonDataFrame[col_names]:
                        tweets += jsonDataFrame[col_names]['id']
            except Exception:
                continue
        # end of for loop

        return tweets