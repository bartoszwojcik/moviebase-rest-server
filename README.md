# 'MovieBase', Django REST server
Sample REST server providing data on movies and cinemas from SQL database. Built using Python, Django and Django-REST-Framework.
Requires authentication with JWT tokens or simple l&p access via the browsable api.

Contains basic tests for GET, POST, UPDATE, DELETE.

Requirements in requirements.txt

# Main features
* Browsable API
* Generic views and models for movies, cinemas, screenings
* Serializers
* API test cases for cinemas, movies, screenings - lists, adding, updates, removal
* Serializer filtering for cinemas: displaying only screenings within the next 30 days
* Search filter for screenings using related movies' names and cinemas' cities
* List pagination
* CORS support
* API root and schema
* Support for requesting .json files directly through URL
* Support for authentication via JWT access tokens, including user serializers


# Sample screenshots

Movie list

![Movie list](screenshots/movie-list.png)

Cinema list with screenings

![Cinema list](screenshots/cinemas-with-screenings.png)

Search results

![Search results](screenshots/search-results.png)

Single screening

![Single screening](screenshots/single-screening.png)


API Root when not logged in

![API-root](screenshots/api-root-no-credentials.png)

**Sample response to token request**

curl -X POST -d "username=bartvessh&password=test123" http://localhost:8000/api-token-auth/

{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImJhcnR2ZXNzaCIsImV4cCI6MTUzODU1ODQ0NSwiZW1haWwiOiIifQ.2Q9P-sJRCkhjn6VqPQ0IJ701QX4StS7zRZ5grjQusEc","user":{"id":2,"username":"bartvessh","is_staff":true}}

# Author
Bartosz Wójcik
bartosz.wojcik@bartvessh.com
