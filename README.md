# nodeflair-scrapper

A simple [Nodeflair](https://nodeflair.com) job scrapper. Specifically to the [search page](https://nodeflair.com/jobs?query=Automation&page=1&sort_by=relevant&countries%5B%5D=Singapore&salary_min=10000).

> Please don't abuse using this!

Idea is like to setup a cron once a day send to your telegram bot for you.

You can read more it [here](https://setkyar.com/scrapping-nodeflair-and-notify-to-telegram).

### Installation

Activate venv and install necesary packages

```
python3 -m venv .venv
. .venv/bin/activate;
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure telegram bot and chat id.

### Usage

```
python main.py <query> <location> <salary>

Example

python main.py DevOps Singapore 8000
```