# Family tree API

This project uses [Flask](https://flask.palletsprojects.com/en/3.0.x/).

## Requirements

| Name | Version |
| ------ |---------|
| Python | ^3.10   |

## Installation

Create .env file

```bash
# .env file format
MYSQL_HOST="localhost"
MYSQL_USER="your_user"
MYSQL_PASSWORD="your_password"
MYSQL_DB="mysql_db_name" #family_tree
MYSQL_TEST_DB = "test_mysql_db_name" #family_tree_test
```

Create databases from family_tree_schema.sql

Install dependencies

```bash
pip install -r requirements.txt
```

## Start webserver

```bash
python app.py
```

## Test

```bash
pytest test_api.py
```
