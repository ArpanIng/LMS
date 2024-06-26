# CustomUser Model Documentation

The `CustomUser` model represents users in the application.

## Managers

### UserManager

The `CustomUserManager` class is responsible for creating users and managing user-related operations.

### Default Group Assignment

By default, users created through the `CustomUserManager` manager directly are assigned to the "Admin" group.

## Proxy Models

### Student

The `Student` proxy model represents users who are students.

#### Manager: `StudentsManager`

This manager is used to create instances of the `Student` proxy model. Users created using this manager are automatically assigned to the "Student" group.

### Instructor

The `Instructor` proxy model represents users who are instructors.

#### Manager: `InstructorsManager`

This manager is used to create instances of the `Instructor` proxy model. Users created using this manager are automatically assigned to the "Instructor" group.

## Custom Management Commands for Creating Groups

This command creates predefined groups in the application.

### Admin Group

```bash
$ python manage.py createadmingroup
```

### Instructor Group

```bash
$ python manage.py createinstructorgroup
```

### Student Group

```bash
$ python manage.py createstudentgroup
```

## Third-party packages command

### Indent templates using the djhtml command

```bash
$ djhtml template.html
```

### python black formatter

```bash
$ black {source_file_or_directory}...
```

### isort specific files

```bash
isort mypythonfile.py mypythonfile2.py
```

### To apply recursively

```bash
isort .
```
