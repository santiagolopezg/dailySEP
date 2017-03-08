## Daily Stanford Encyclopedia of Philosophy (@dailySEP)
I made a little tweet bot that posts daily entries from the Stanford Encyclopaedia of Philosophy. 

It's just a quick project, based on a few blog posts I read ([Brian Caffey's post](http://briancaffey.github.io/2016/04/05/twitter-bot-tutorial.html) helped a lot). 
I really enjoy Wikipedia's twitter account, which posts random (*very random*) entries daily. I also love reading the [Stanford Encyclopaedia of Philosophy](https://plato.stanford.edu/), 
and thought it'd be a cool project to create a bot that randomly posts entries from the SEP. You can check it out [here](https://twitter.com/dailySEP).       
       
It's is still greatly a work in progress, and I hope I can get it to do more cool stuff shortly!        
       
I've included essentially the code I run on [Heroku](https://devcenter.heroku.com/categories/python), but removed the Twitter security keys
and access codes. These are generated per account, so they're a pretty big deal.        
I would recommend you to write your own bot, because it's quite easy, and you learn a lot in the process. I enjoyed learning about Heroku 
and Tweepy, as well some basic html manipulation with Python libs.      
However, if you'd like to try it, just download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install), sign up, setup
your account locally and clone this repo. Then, you can `cd ~/dailySEP` and `heroku create` (remember to change the `config.py` file). That basically creates a dyno (yeah I know, 
but do read the docs) which can be set up to run remotely. If you want to play around with it first, I'd advise you run it locally (follow [these
steps](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)), and when you've got that settled, do:
`cd ~/dailySEP` -> `heroku ps:scale worker=1`       
That should set it up to work remotely. You can check the logs: `heroku logs --ps worker` and also stop it: `heroku ps:stop worker.1`.
      
All in all, *just read the docs!* (some listed below)  

                 
![Yes, documentation](http://a.memegen.com/jy0j99.gif)             
             
### Useful links:
- [Brian Caffey's post](http://briancaffey.github.io/2016/04/05/twitter-bot-tutorial.html)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
- [Heroku: scaling dyno formation](https://devcenter.heroku.com/articles/scaling)
- [Heroku: Process types and the Procfile](https://devcenter.heroku.com/articles/procfile)
- [Heroku: dynos / configs](https://devcenter.heroku.com/articles/dynos#the-dyno-manager)
