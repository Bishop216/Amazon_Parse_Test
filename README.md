# Amazon ASIN Parser

### Running api (development):
Export flask environmental variables and run it:
```bash
export FLASK_APP=application
export FLASK_ENV=development
flask run
```

### Initializing DB tables:
```bash
flask db init
flask db migrate
flask db upgrade
```

### API endpoints:
    "/parser/upload" - POST
    Excepts a csv file with Amazon asins.
    Parses out asin product info and saves it to DB.