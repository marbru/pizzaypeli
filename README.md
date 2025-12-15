# Pizza y Peli

A simple app to plan and keep track of our home cinema sessions.

<img src="claude_log/8.png" style="max-width:700px; width:100%;" />

Made with Django, and mostly vibecoded with Claude and Cursor. I'm trying to keep a log of the prompts used at [claude_log/prompts.md](claude_log/prompts.md)

Uses https://github.com/tveronesi/imdbinfo to fetch movie metadata (no API keys required)

## Install

```pip install -r requirements.txt```

## Housekeeping

Run the app:

`python manage.py runserver`

Handle migrations:

```
python manage.py makemigrations # to create migrations for model changes
python mange.py migrate # to apply the changes to the DB
```

Django shell:

`python manage.py shell`

Add new dependencies:

`pip freeze > requirements.txt`

