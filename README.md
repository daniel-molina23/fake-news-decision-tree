# CS 4800 - Local Web API with integrated Fake News Decision Tree Classifier Repo

- TODO:
    - deploy Flask Application to Heroku - done!
    - Teach Daniel deployment
    - take twitter API JSON files and improving JSON extraction class(JsonParser.py)

- Description
    - Taking JSON from twitter API, inputing into local server, extracting, cleaning/encoding data and finally computing fake news/real news with decision tree models

- Dependencies
    - pip install:
        - pandas, sklearn, requests_html, flask
    - get 'PostMan' app and use tweetFromGit.json to send data to local server 
    - you can now send requests from Postman to https://fake-news-dt-app.herokuapp.com/api/v1/webApp