To run app from project dir:

### ATTENTION: Install postgresql if needed

```python3 -m venv venv```

```source venv/bin/activate```

```pip3 install -r requirements.txt```

```sudo psql -U $USER -d postgres -f init.sql```

```./manage.py migrate```

```./manage.py runserver```
