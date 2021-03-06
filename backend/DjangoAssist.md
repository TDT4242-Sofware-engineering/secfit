To access Django application from terminal:
`python manage.py shell`

Accessing user objects
```python
from django.contrib.auth import get_user_model

# Retrieve all users
users = get_user_model().objects.all()

# Retrieve specific user
donald = get_user_model().objects.filter(username="donald")

# Print all values
donald.values()
```