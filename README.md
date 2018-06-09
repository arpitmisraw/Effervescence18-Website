# Effervescence18-Website

## To run locally

1. cd into the repository root folder.
2. Run virtualenv
3. Type sudo pip3 install -r requirements.txt
4. Type python3 manage.py runserver


## Url structures

### Authentication is done using the django-rest-auth library. Following are the end-points:

Login - /api/login/
Logout - /api/logout/
Password Change - /api/password/change/
User details - /api/user/
Register new user - /api/registration/


### For social authentication, the login access token has to be provided(PUSH) to the following end-point:

/auth/convert-token/

### which would return a local access token that needs to be provided in header for every request.
