# Project Overview
simple-blog-cms is *surprise*, *surprise* a simple content management platform for blogs.  

If you want to publish your ideas to the internet right now, you either have to use a platform like Facebook, Twitter, Medium, or Squarespace; or you have to put in a lot of work (and know a fair amount of technology) to build it yourself. Neither of these is ideal.

This project seeks to bridge the gap between those two worlds to create an idependent blogging solution that the user near complete control over, but that anyone can spin up with minimal set up.
  
# How does it work  
Essentially, this is a Flask app that writes "posts" to JSON files, creating a simple NoSQL database -- and then reads from that file to display the posts. My goal was to create this using as few additional packages as possible.

# What's included in this repo  
Below is a quick tour of the files and directories in this repo:  
+ app.py  
    - This file handles routing and does most of the heavy lifting in the code. At some point, I would like to make this more modular.
+ data/  
    - blog_info.json - contains global information about the blog - user credentials, blog name, tagline, author name and bio
    - posts_metadata.json - contains metadata about posts, to aid in displaying lists of all posts
    - posts.json - contains content of individual posts 
+ models/
    - auth.py - Contains functions for hashing passwords and checking user credentials
    - forms.py - Contains classes used to create forms
    - PostObject.py - an object used to create and manipulate posts
+ static/
    - 
+ templates/
    - This directory holds the various HTML files 

# Requirements
- Python
- Flask
- WTForms


# How to start the flask app
> $ export FLASK_APP=app.py  
> $ export FLASK_ENV=development  
> $ flask run  
Then point browser to localhost:5000  

# How to deploy
TODO

# How to reset your password
TODO


