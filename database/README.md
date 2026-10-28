# Database
The app uses `Qsr_Queue_Database` by default in Docker. The application creates only its own `qsr_*` tables using additive `CREATE TABLE IF NOT EXISTS` semantics through SQLAlchemy metadata. It never drops or recreates the database.

For production:
1. Back up the database.
2. Inspect existing schema and ownership.
3. Use reviewed Alembic migrations.
4. Verify pre-existing tables and records after migration.
5. Restrict the DB account to least privilege.

Do not store real credentials in this directory or source control.
