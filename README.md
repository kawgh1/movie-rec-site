# movie-rec-site
flask movie recommender site using cosine similarity

### note: site is a bit slow because it is calling machine learning algos on a large hosted database of 10,000+ movies, 100,000+ user reviews and 1,000+ movie tags. 
#### Ideally GPUs like Google CoLab or other cloud processors would be used to make requests in milliseconds 

To access the publicly hosted version of the application on Heroku, visit https://hr-movie-rec-site.herokuapp.com/home . Note this version’s databases are hosted on Heroku and the data displayed on its dashboard will differ from that on the local host dashboard.



Requirements
To successfully run the application locally, the following software is required:
	Windows 10 OS – Windows 7 and 8 should be viable, but not guaranteed – some dependencies listed in requirements.txt are Windows specific. The application was not tested on other operating systems.
	Python v. 3.6+ older versions are incompatible with some of the required dependencies. 3.7+ may not be supported by all webservers in deployment.
	PostgreSQL 10 – newer versions are incompatible with some of the required dependencies

Recommender Engine 
To run the application on a localhost, run these commands in the terminal once you have opened the application folder:
1.	python3 -m venv venv
2.	venv\Scripts\activate
3.	pip install -r requirements.txt
4.	python run.py



You should now see displayed in your terminal the familiar Flask bootup dialog:

 * Serving Flask app "movieRecFlask" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: ###-###-###
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


Either click the link in the terminal or copy the address into your web browser. You should be taken to the main recommender page that reads “Movie Recommender: What’s Next?”
The default settings in ‘run.py’ and ‘dashboard1.py’ are for the localhost. For a production server, the settings listed at the top of those two files must be switched out as directed.
To access the publicly hosted version of the application on Heroku, visit https://hr-movie-rec-site.herokuapp.com/home . Note this version’s databases are hosted on Heroku and the data displayed on its dashboard will differ from that on the local host dashboard.
