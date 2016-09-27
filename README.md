# My Multi User Blog

This app is currently live at http://my-multi-user-blog.appspot.com

#### How to run this app

If you'd like to download from source and run, please take the following steps:

* Make sure you have Python 2.7 installed. If you need to get it, go here for the (as of 9/27/16) latest version: https://www.python.org/downloads/release/python-278/
* Make sure you have the Google Cloud SDK for Python 2.7.x installed. If you need to get it, go here: https://cloud.google.com/sdk/docs/
* Download (it will be a zip, so unzip it wherever you choose) or use git to clone this project (to wherever you want) from Github
    * If you downloaded it: After unzipping, you will get a folder that should be called "my-multi-user-blog-master"
    * If you used git to clone this project: You will get a folder that should be called "my-multi-user-blog"
* To run the app locally using Google Cloud's local development environment, you will need to open a terminal and navigate to the directory where the project folder is located.
    * Example: If you downloaded it to your "Downloads" folder, open your terminal and navigate to your "Downloads" folder.
* In your terminal, type the following and then hit enter: dev_appserver.py {project folder name}
    * Example, if the project folder name is my-multi-user-blog-master, type: dev_appserver.py my-multi-user-blog-master
* You will see something like the following two lines in the terminal once the app is ready to be used:
    * Starting module "default" running at: http://localhost:8080
    * Starting admin server at: http://localhost:8000
* When you see this, open up your browser and navigate to the address in the line that mentions "default" which will most likely be http://localhost:8080
* Enjoy!
