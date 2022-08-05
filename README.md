# Flask Web

Flask web application boilerplate

## Development

1. Set environment variables

```
FLASK_APP=web.app
FLASK_DEBUG=1
FLASK_ENV=development
FLASK_RUN_HOST=localhost
FLASK_RUN_PORT=80
DATABASE_URL=sqlite:///../db.sqlite3
SECRET_KEY=secret
```

1. Initialize database

```
flask db init
flask db migrate
flask db upgrade
flask insert
```

1. Run dev server

```
flask run
```

## PyCharm Configuration

![PyCharmConfiguration](https://i.imgur.com/9f21iNs.png)

1. Copy the environment variables above
1. Create a run configuration as shown and paste the variables
1. Open Settings > Tools > Terminal and paste the variables

## Docker
```
docker build -t web .
docker run -d -p 80:5000 --name web web

docker stop web
docker rm web
docker image rm web
```

## Docker Compose

Create web and Postgres containers. Mount Postgres to `/data` for persistence.

1. Start containers

```
docker compose up -d
```

1. Initialize database

```
docker compose exec web bash
flask db migrate
flask db upgrade
exit
```

1. Teardown

```
docker compose down
docker image rm web
```

## Test

1. Lint

```
flake8 --count --max-line-length=120 --max-complexity=10 --exit-zero --statistics
```

1. Test

```
pytest
```
