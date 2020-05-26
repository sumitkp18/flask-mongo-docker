## Dependencies
> * python3
> * docker

## SETUP instructions for docker
### (for non-docker env follow the next setup instruction for python virtual env)
1. create a file in root directory (flask_mongo_docker/) with name: ".env"
    >$touch .env
2. add the following keys to the ".env" file
	>JWT_SECRET_KEY='jwt_secret_key'
	host ='0.0.0.0'
    port='5000'
3. build docker:
	> $ docker-compose build
4. run docker
	> $ docker-compose up

## SETUP instructions for python-venv setup (required for development)
### MongoDB:
1. Install mongodb
2. open terminal and run it:
	> $ mongod

### Python:
1. create a python virtual environment in the root directory (same level as docker-compose file)
	>python -m venv <virtual_env_name>
	eg: $ python -m venv  flask_env

2. activate the virtual environment
	>eg:	$ . flask_env/bin/activate
	
	NOTE: mind the space between  . (dot) and flask_env (env name)
	(you can see the virtual env name at the beginning of the shell)

3. install python dependencies in your env.
	> eg: $ pip install -r requirement.txt

4. define 3 environment variables t):
    > $ export ENV_FILE_LOCATION=$(pwd)'/.env'
    $ export MONGODB_HOST='localhost'
    $ export MONGODB_NAME='flask_app'

5. Now you can run the flask app:
	> $ cd flask_app
	$ python app.py


## APIs:
1. ### Signup:
	* endpoint:
		>	localhost:5000/api/auth/signup
	
	* 	body: 
		> {
			"email": <email>,
			"password": <password>,
			"first_name": <first name>,
			"last_name": <last name>
		}

2. ### Login:
	* endpoint: 
	> localhost:5000/api/auth/loginbody: 
	
	* body:
	>	{
			"email": <email>,
			"password": <password>,
			}

3. ### New Access Token:
	* endpoint:
		> localhost:5000/api/auth/refresh
	
	* authorization:
		>bearer token: refresh_token

4. ### Logout with access token
	* endpoint: 
		> localhost:5000/api/auth/logout_access
	
	* authorization:
		> bearer token: access_token

5. ### Logout with refresh token
	* endpoint:
		> localhost:5000/api/auth/logout_refresh
	
	* authorization:
		> bearer token: refresh_token
