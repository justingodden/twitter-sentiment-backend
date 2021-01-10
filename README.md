# Sentient - backend API and ML
Twitter sentiment analysis app backend, hosted on Heroku.

The app provides a dashboard which can give a weeks analysis of the the public sentiment of your search-term, according to Twitter.

It is able to run on either HuggingFace's Transformers package, and NLTK's Vader algorithm. The [deployed version](https://justingodden.github.io/twitter-sentiment-frontend/) uses Vader, as Transformers' filesize are too large for the free tier on Heroku.

The classifier is wrapped in a Flask web application, providing an API end-point for the [front-end interface](https://github.com/justingodden/twitter-sentiment-frontend).

Below are some gifs of it in action.

![GitHub Logo](/github_images/mobile.gif)

![GitHub Logo](/github_images/1080p.gif)
