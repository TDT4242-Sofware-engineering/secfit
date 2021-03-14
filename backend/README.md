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

After running test with `coverage`, run one of these commands to generate a report:

Create list report:

```bash
coverage report
```

Create HTML report:

```bash
coverage html
```