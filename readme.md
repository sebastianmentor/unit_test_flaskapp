# Lindas Lustfyllda bokhandel
Added some shady testing

## envrionment
Create a environment
```bash
py -m venv my_environment
```
Activate it
```bash
.\venv\Scripts\activate
```
Install requirements
```bash
pip install -r requirements.txt
```

Create a .env file 
```python
# Security 
SECRET_KEY = 'Your secret key'
SECURITY_PASSWORD_SALT = 'Your password salt'

# Databses
SQLALCHEMY_DATABASE_URI_LOCAL = 'mysql+mysqlconnector://root:password@localhost/LLB'
```

Run app:
```bash
py app.py
```

Run Test:
```bash
py test.py
```