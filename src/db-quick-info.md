# PostgreSQL refference

## Creating a database, user and granting permissions

```sql
create database database_name;
create user username with encrypted password 'password';
grant all privileges on database database_name to username;
```

## Connecting to a database

```sql
\connect database_name
```

The backslash here is crucial.

## Creating a table

```sql
CREATE TABLE table_name (
   column_name TYPE column_constraint,
   table_constraint table_constraint
);
```

See [https://www.postgresqltutorial.com/postgresql-create-table](https://www.postgresqltutorial.com/postgresql-create-table)
