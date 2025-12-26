# ETL Example with Postgres

This project demonstrates a minimal **Extract–Transform–Load (ETL)** pipeline that pulls data from a public API, transforms it with **pandas**, and loads it into a **Postgres** database.

---

## 1. Database Setup (via pgAdmin)

### Step 1: Connect to your local Postgres server
- Open **pgAdmin** and log in with the password you set during installation.

### Step 2: Create a database
- Right-click **Databases → Create → Database**.  
- Name it **`mydb`** (to match `dbname="mydb"` in the script).  
- Leave the owner as your Postgres superuser (commonly `postgres`) or the role you plan to use.

### Step 3: Create a login role (user)
- Navigate to **Login/Group Roles → Create → Login/Group Role**.  
- In the **General** tab: name it **`myuser`**.  
- In the **Definition** tab: set password **`mypassword`** (must match the script).  
- In the **Privileges** tab: check **Login**, and optionally **Create DB** for flexibility.  
- In the **Membership** tab:  
  - Add this role to `pg_read_all_data` / `pg_write_all_data` if available.  
  - Otherwise, grant privileges manually (see below).

### Step 4: Grant privileges on the database
- Expand the **mydb** database → go to **Properties → Privileges**.  
- Add your new role `myuser` with:
  - **CONNECT**
  - **CREATE**
  - **TEMP**
  - **ALL privileges**

### Step 5: Sanity check
Open a query tool on **mydb** and run:

```sql
\c mydb myuser
SELECT current_database(), current_user;
````

Expected output: `mydb / myuser`.

---

## 2. Minimal Install & Run

### Requirements

Create a `requirements.txt` with:

```
pandas==2.2.2
psycopg[binary]>=3.1,<3.3
requests==2.32.3
```

### Virtual Environment (Windows, Python 3.12 recommended)

```powershell
python -V           # if this says 3.13, create a 3.12 venv
py -3.12 -m venv venv312
.\venv312\Scripts\Activate.ps1
python -V           # should say 3.12.x

# Upgrade pip/setuptools
python -m pip install -U pip setuptools wheel

# Install dependencies
pip install -r requirements.txt
```

---

## 3. Running the Script

Before running:

* Ensure **Postgres is running locally**.
* A database named **mydb** exists.
* The role **myuser/mypassword** is valid and has the correct privileges.
* The port in the script matches your server’s port.

When executed, the script:

1. Creates the table `posts` if it does not already exist.
2. Pulls rows from the public API.
3. Loads them into **Postgres**.

---

## Notes

* If `pg_read_all_data` / `pg_write_all_data` memberships are not available, grant privileges directly:

  ```sql
  GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
  ```
* See the main repo README for further details on permissions and roles.
