## Popular Github Repositories

### How to set up

Create a `.env` file providing the following attributes:

```
GITHUB_ACCESS_TOKEN=your_access_token
POPULAR_BASE_SCORE=500
DJANGO_SECRET_KEY=your_django_secret_key
```

### Getting an access token do the following:

* Open https://github.com/ and log in
* Click your user icon and follow this path `Settings / Developer settings / Personal access tokens`
* Click on `Fine-grained tokens` and click on `generate new token`

### Running the application

With Docker running, execute the following command in a terminal:

`docker-compose up -d --build`

Once the command is finished, open your browser and paste the 
url http://0.0.0.0:8000/api/health_status to check the application health status.

It is also possible to check the API swagger schema in the following url:

http://0.0.0.0:8000/api/docs/

To run the tests, execute the following command:

`docker-compose exec web pytest`
