# 📚 About 

Subscribes to a specific UTK course and sends you an email when a seat is available.

# 📝 Requirements

The project uses docker for maximum portability, in which case you can deploy it anywhere that supports docker. If you don't want to use docker, goto the [alternative](#alternative---no-docker) section.

- Docker
- Docker Compose (optional)

## Alternative - No Docker

### Pip

All requirements are listed in the `requirements.txt` file. You can install them with `pip install -r requirements.txt`.

### Poetry

You can also use [poetry](https://python-poetry.org/) to install the dependencies. 

```bash
poetry install
```

### Python

Python is of course required. 3.10 is recommended, but other versions might work. I have not tested. If you are using Poetry, it assumes you have Python 3.10 or greater installed.

# 🚀 Usage

When you run the program, it will subscribe to the courses in the watchlist and send you an email when a seat is available. Otherwise, it will just keep running and checking every minute. This can be tweaked in the source code if you want a longer/shorter interval.

A duo authentication push notification will be sent to your phone periodically when the cookies need to be refreshed. If it's not accepted within one minute, it will retry. This process is repeated until the cookies successfully refresh.

## 🐳 Docker

```bash
docker-compose up -d
```

### 🔑 Environment Variables

Environment variables can be defined in the `docker-compose.yml` file, in an `.env` file, or in your computer's environment itself. 

| Variable | Description | Default |
| --- | --- | --- |
| `EMAIL` | Email to send notifications to | `undefined` |
| `EMAIL_PASSWORD` | Password for your email | `undefined` |
| `USERNAME` | UTK NetId | `undefined` |
| `PASSWORD` | UTK Password | `undefined` |

Email must be a gmail account, but can be modified in the source code if you want to use a different email provider. The email password must also be an app password, which can be generated [here](https://myaccount.google.com/apppasswords).

#### example `.env` file

```bash
USERNAME=myusername
PASSWORD=mypassword!
EMAIL=foo@gmail.com
EMAIL_PASSWORD=myemailpassword
```

#### Watchlist

The watchlist is defined in the `watchlist.txt` file. It simply lists the courses that will be subscribed to. The required format is the course abbreviation, followed by a space, followed by the course number. For example, `COSC 101` or `MATH 241`.

## 🐍 Python


### No Poetry

```bash
python check.py
```

### Poetry

```bash
poetry run python check.py
```

## Personal Note

Personally, I host this project for myself on [Railway](https://railway.app/). It's a free hosting service that supports docker, and it's extremely easy to set up. You can fork this repo, and then deploy it to Railway with one click straight from GitHub. The environment variables can be set in the Railway dashboard as well (since you won't want your .env file to be public).
