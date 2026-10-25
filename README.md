# Little Lemon Restaurant API

A Django 5 and Django REST Framework capstone for the Little Lemon restaurant.

## Windows setup

From the project directory in the VS Code PowerShell terminal:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once in that terminal.

The default configuration uses SQLite so the project can run immediately. For MySQL, create a database (`CREATE DATABASE littlelemon CHARACTER SET utf8mb4;`), set `DB_ENGINE=mysql` and the `MYSQL_*` values in `.env`, then run `python manage.py migrate`. The included `mysqlclient` package is the MySQL driver. Verify either database connection with `python manage.py check` and `python manage.py migrate`.

Never commit `.env`; it is excluded by `.gitignore`.

## API

All API paths are listed in [Readme.txt](Readme.txt). Menu reads are public. Menu writes and every booking operation require `Authorization: Token <token>`. Register and login are public.

Example menu body:

```json
{"title": "Greek Salad", "price": "12.50", "inventory": 10}
```

Example booking body:

```json
{"name": "Sam", "no_of_guests": 2, "booking_date": "2030-06-15T19:00:00Z"}
```

## Testing

```powershell
python manage.py test
```

Use Django admin at `/admin/` to add sample menu items, or create them with an authenticated `POST`.

## GitHub

```powershell
git init
git add .
git commit -m "Build Little Lemon restaurant capstone"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your GitHub repository URL.
