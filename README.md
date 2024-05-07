## Create superuser

```
python manage.py createsuperuser
```

## Create Groups

[Link to Commands](COMMANDS.md)

## Provide initial data for models

### For CustomUser Model

```
python manage.py loaddata db_customuser.json
```
> All passwords from the fixture file 'db_customer.json' are `superuser`

### For Category Model

```
python manage.py loaddata db_category.json
```

### For CourseLevel Model

```
python manage.py loaddata db_courselevel.json
```

### For Language Model

```
python manage.py loaddata db_language.json
```

### For Course Model

```
python manage.py loaddata db_course.json
```
