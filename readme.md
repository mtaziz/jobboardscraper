# Job board scraper

This code scrapes a job board with [Scrapy](http://scrapy.org/) every day and integrates it into a [Django](https://www.djangoproject.com/) website with an [Elasticsearch](http://www.elasticsearch.org/) search index and a [PostgreSQL](http://www.postgresql.org/) database. The website is hosted on [Heroku](https://www.heroku.com/).

The deployed website: [http://timgorin.herokuapp.com](http://timgorin.herokuapp.com/)

## Installation

Prerequisites: [Python](https://www.python.org/), [PostgreSQL](http://www.postgresql.org/), [Pip](https://pip.pypa.io/), [virtualenv](http://virtualenv.readthedocs.org/), [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/), and [Git](http://git-scm.com/).

You will need to [generate](http://www.miniwebtool.com/django-secret-key-generator/) a [`SECRET_KEY`](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key) environment variable to run the website. Append `export TIMGORIN_SECRET_KEY='...'` to `~/.bash_profile` and restart Terminal.

1. `mkvirtualenv timgorin`
2. `git clone git@github.com:richardcornish/timgorin.git`
3. `add2virtualenv timgorin`
4. `cd timgorin`
5. `pip install -r requirements.txt`
6. `python manage.py syncdb`
7. `python manage.py runserver`
8. Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Scrape

To run the spider to scrape the website:

```
cd scraper && scrapy crawl eslcafe
```

## Search

Elasticsearch (and thus Java) is required to update the search index. Assuming [Homebrew](http://brew.sh/) is installed:

1. Install [Java JDK and Java JRE](http://www.oracle.com/technetwork/java/javase/downloads/index.html)
2. `brew install elasticsearch`
3. `elasticsearch --config=/usr/local/opt/elasticsearch/config/elasticsearch.yml`
4. `python manage.py rebuild_index` (or `python manage.py update_index` subsequent times).

## Heroku notes

Heroku requires some [environment variables](https://devcenter.heroku.com/articles/config-vars):

```
heroku config:set TIMGORIN_SECRET_KEY='...'
heroku config:set DJANGO_SETTINGS_MODULE='timgorin.settings.production'
heroku config:set WEB_CONCURRENCY='2'
```

Heroku add-ons I used:

- [Heroku Postgres](https://addons.heroku.com/heroku-postgresql)
- [Heroku PG Backups](https://addons.heroku.com/pgbackups)
- [Heroku Scheduler](https://addons.heroku.com/scheduler)
- [SearchBox Elasticsearch](https://addons.heroku.com/searchbox)

The Scheduler needs to run these tasks every day to scrape the website and update the search index:

- `(cd scraper && scrapy crawl eslcafe)`
- `python manage.py update_index`

You might need to edit the [SearchBox settings](https://dashboard.searchly.com/6886/indices) on your Heroku dashboard to manually register your SearchBox API key and your search index's name.

If you're running commands straight on Heroku:

- `heroku run '(cd scraper && scrapy crawl eslcafe)'`
- `heroku run python manage.py update_index`
- `git push heroku master`

## Resources

Resources that helped me:

- [hk0weather](https://github.com/sammyfung/hk0weather) Hong Kong weather data project by [Sammy Fung](http://sammy.hk/)
- [Python, Web scraping and content management: Scrapy and Django](http://www.slideshare.net/sammyfung/python-web-scraping-and-content-management-scrapy-and-django)
- [Open Data, Open Government](http://www.slideshare.net/sammyfung/hk0weather-barcamp)
- New Coder "[Web scraper](http://newcoder.io/scrape/)" tutorial by [Lynn Root](http://www.roguelynn.com/)
- [Getting started with Django on Heroku](https://devcenter.heroku.com/articles/getting-started-with-django)
