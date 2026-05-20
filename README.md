# todo fastapi pgsql

```
# 1. Update model in api/app/models/
class User(Base):
    # ...existing fields...
    new_field = Column(String)  # Add new column
# 2. Auto-generate migration
alembic revision --autogenerate -m "your_change_description"

# 3. Review generated file in api/alembic/versions/
# 4. Apply migration locally
alembic upgrade head

# 5. Commit migration file to git
git add api/alembic/versions/
git commit -m "Add migration: your_change_description"
```