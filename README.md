# Sentient - backend API and ML
Twitter sentiment analysis app backend

The app provides a dash board which can give a weeks analysis of the the public sentiment of your search-term, according to twitter.

It is able to run on either HuggingFace's Transformers package, and NLTK's Vader algorithm. The deployed version uses Vades, as Transformers are too large for the free tier of Heroku.

The classifier is wrapped in a Flask web application, providing an API end-point for the [front-end interface](https://github.com/justingodden/twitter-sentiment-frontend).

Below are some gifs of it in action.

![GitHub Logo](/github_images/mobile.gif)

![GitHub Logo](/github_images/1080p.gif)
