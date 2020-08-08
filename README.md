# COMP-353-Main-Project

## Set Up
* install python 3 (latest version)
* git clone this repository
* cd to project folder and install dependencies: 
  * `pip install flask` or `pip3 isntall flask`  depending on your python installations
  * `pip install sshtunnel`
  * `pip install pymysql`
  * `pip install python-dotenv`
### Environment File
* Make an `.env` file on the root directory, inside you should include:
 
 `ENCS_USR=YOUR_ENCS_USERNAME`
 
 `ENCS_PWD=YOUR_ENCS_PASSWORD`

 `DB_USR=oxc353_1`

 `DB_PWD=bobatea1`

## Starting the App
* cd into folder and write in terminal  `python app.py` to start the web app
* open up default browser search `localhost:5000`
