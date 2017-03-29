# KRI Regional 3 2017

[![Build Status](https://travis-ci.com/ilhamadun/kri.svg?token=HfSF5qs9S26Nqtb4fu4e&branch=master)](https://travis-ci.com/ilhamadun/kri)

Website Kontes Robot Indonesia Regional 3 2017 Universitas Gadjah Mada.

### Contribution Guides

Before commiting, make sure you:
- Pass all tests with `python manage.py test`
- Run `pylint` over your code. Only suppress warnings if they are inappropriate

### Installation

```shell
git clone https://github.com/ilhamadun/kri.git
cd kri
pip install -r requirements.txt
```

### Development Server

First, assign the configuration file to environment variable:

```shell
export DJANGO_SETTINGS_MODULE=kri.settings.local
```

Run the development server:

```shell
python manage.py runserver
```

If you want to listen on public IP, use:

```shell
python manage.py runserver 0.0.0.0:8000
```