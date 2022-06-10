



# Customer Relationship Management(CRM) Application

## Objectives:
- Develop a secure application with PostgreSQL
- Create an API where different user interacts with the database 
- The application is created with django and django rest framework with simpleJWT as a default authentication
- Manage the authorisation or permission with different user(manager, sales contact and support contact) with django-admin interface



## Application environments:
 - python: version 3.8
 - django: 4.0
 - postgreSQL >=12


## Getting started:
### DATABASE CONFIGURATION
**Note**: Make sure you have postgreSQL on your machine, you can check it with `psql --version` to see the version or click [here](https://www.postgresql.org/download/) to download and read the documentation how to launch the database server.

After lauching the postgreSQL:
 -  Create a database with `crm` as name of the database



### DJANGO CONFIGURATION
**Note**: Make sure you have python(atleast version 3.8) , virtual environment and git on your machine:
	- `python -V` : command to check the version python if its installed
	- verify that you have the venv module : `python -m venv --help` if not please check https://www.python.org/downloads/. You could also use any other virtual environment to run the program(**if you opted to use other virtual environment the next commands are not suitable to run the program**)
	- `git --version` : to check your git version if its installed or you could download it at https://git-scm.com/downloads
 1. Clone the repository on the terminal or command prompt : `git clone https://github.com/jheslian/epic_events.git`
 2. Create a virtual environment with "venv"  
	 - `cd epic_events` :  to access the folder 
	 - python -m venv ***environment name*** : to create the virtual environment - exemple: `python -m venv env`
3. Activate the virtual environment:
	for unix or macos:
	- source ***environment name***/bin/activate - ex : `source env/bin/activate` if "env" is used as environment name 
	for windows:
	- ***environment name***\Scripts\activate.bat - ex: `env\Scripts\activate.bat`
4. Install the packages with pip: `pip install -r requirements.txt`	
5.  Migrate the tables to database:
	- for unix or macos: `python3 manage.py migrate`
	- for windows: `py manage.py migrate`
6.  Create an administrator:
	- for unix or macos: `python3 manage.py createsuperuser`
	- for windows: `py manage.py createsuperuser`
7. Run the program :
	- for unix or macos: `python3 manage.py runserver`
	- for windows: `py manage.py runserver`
	***Note*** : The default port will open at 8000.



## How the application works:
***note:*** The database and django must be launch before
1.  Login as administrator on django admin interface with the url: ` http://127.0.0.1:8000/admin`
		
2. Create 3 differents groups(management, sales and support) for your user and add the specific permission on on each group to specify their authorisation on the application
	* management
    
	[![Screenshot-2022-06-10-at-09-13-31.png](https://i.postimg.cc/65f4GRj9/Screenshot-2022-06-10-at-09-13-31.png)](https://postimg.cc/tY74K1Gf)
	* sales
    
	[![Screenshot-2022-06-10-at-09-15-12.png](https://i.postimg.cc/t4fq14jq/Screenshot-2022-06-10-at-09-15-12.png)](https://postimg.cc/TKVMFG1F)
	
	* support
    
	[![Screenshot-2022-06-10-at-09-16-05.png](https://i.postimg.cc/4N2ZMxn6/Screenshot-2022-06-10-at-09-16-05.png)](https://postimg.cc/LnPrgRt5)
3. For a user to have an account, an admin or a manager must create an account for them and assign which group they belong and provide them the login and latter the user could change their password.
4. Check the API documentation provided on how to use the API and see some examples : [Epic Events API](https://documenter.getpostman.com/view/19593881/Uz5MFZqd)
