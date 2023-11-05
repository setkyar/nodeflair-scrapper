# nodeflair-scrapper

A simple [Nodeflair](https://nodeflair.com) job scrapper. Specifically to the [search page](https://nodeflair.com/jobs?query=Automation&page=1&sort_by=relevant&countries%5B%5D=Singapore&salary_min=10000).

> Please don't abuse using this!

Idea is like to setup a cron once a day send to your telegram bot for you.

You can read [this blog post](https://setkyar.com/scrapping-nodeflair-and-notify-to-telegram) for usage idea. Nothing new as here but writing as a blog post lol!

### Installation

Activate venv and install necesary packages

```
python3 -m venv .venv
. .venv/bin/activate;
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure telegram bot and chat id.

```
NOTIFY_TELEGRAM=False
TELEGRAM_BOT_TOKEN=Your bot token without bot prefix
CHAT_ID=
```

Don't forget to download [geckodriver](https://github.com/mozilla/geckodriver/releases) and move it under `~/.local/bin` and make it executable.

### Usage

```
python main.py <query> <location> <salary>

Example

python main.py DevOps Singapore 8000
```