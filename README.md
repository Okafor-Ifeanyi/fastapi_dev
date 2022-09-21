FastApi

This is my best framework for developing apis, as the name implies fastapi is fast and simple
setting up a blog on this wont take you more that 50 lines of code(without auth).

Breif Narration:
What your looking at is a Blog, containing majorly Users, Posts, and Votes
User are created as they are registered by people 
Posts are created by users which are viewed by everyone, only users can create post but everyone can view a post
Votes are likes on a particular post, 1 like granted per User on a post, makes Users & Post a joint primary key

Postgres handles the data and storage 
JWT Auth handles the Authentication(where you can and can not access depending on your role)
Python is the language the Fastapi was built on


The project here is an explicit combination of how a full fleshed api can be built using Fastapi, 
python, Postgres, JWT auth, github workflow, pytest and other basic functions.
