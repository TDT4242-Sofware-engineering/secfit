# Development

Start development:

```bash
python secfit/manage.py runserver
```

# Tests
Run tests, from `backend/secfit`:
```bash
python ./manage.py test --pattern="tests.py"
```

With coverage:
```bash
coverage run --source='.' manage.py test
```

Create report:

```bash
coverage report
```