# Rationale for id and uid

In the provided code, both id and uid are used as identifiers for database records, but they serve different purposes:

## id (Integer Primary Key)
### Rationale
- id is an integer field typically used as the primary key in a database table.
- Relational databases are highly optimized for integer primary keys.  They are efficient for indexing, joining tables, and overall performance.
- Many Object-Relational Mappers (ORMs), like SQLModel/SQLAlchemy,default to using integer primary keys.
- Auto-incrementing integers are simple to generate and ensure uniqueness within a table.

### Best Practices
- Internal Use: Use id primarily for internal database operations. This includes:
    - Joining tables in database queries.
    - Referencing records in other tables (foreign keys).
    - Efficiently retrieving records by their primary key.
- Don't Expose Directly: Avoid exposing id directly in your API endpoints or URLs whenever possible.  This prevents potential security issues, such as users guessing or manipulating IDs to access unauthorized data.  It also decouples your API from your database schema, making it easier to change the latter without breaking the former.

## uid (UUID)
### Rationale
- uid is a UUID (Universally Unique Identifier) field.
- UUIDs are designed to be globally unique, meaning the probability of generating the same UUID twice is extremely low, even across different systems or databases.
- They are useful for identifying records in a distributed system where multiple databases might be generating new IDs.
- They enhance security by making it more difficult for attackers to guess or manipulate identifiers.

### Best Practices

- External Use: Use uid for identifying records in your API endpoints, URLs, and when communicating with external systems. For example:
    - Include the uid in the URL to identify a specific resource (e.g., /accounts/{uid}).
    - Return the uid in API responses when representing a resource.
    - Use the uid in client-side applications to reference resources.
- Security: Because UUIDs are long and random, they are much harder to guess than sequential integers, making your API more secure.
- Obfuscation: Using a uid instead of the id can also help prevent information leakage about the number of records in your database.  For example, if your user IDs are sequential integers, an attacker might be able to infer how many users you have.
- Flexibility: UUIDs are not tied to a specific database, which makes them suitable for use in distributed systems or when migrating data between databases.