## Python-preparation Steps for running the program on your machine:

NB:
(connection_stuff.py is not checked in to github and must be created by you --> see private_stuff.py for info)

1. Create a virtual environment:

```
python3 -m venv venv
```

2. Activate it:  [This step is repeated anytime you want this venv back]

```
source venv/bin/activate
```

On windows you would do:

```
venv\Scripts\activate
```
If no permission in Windows
 The Fix (Temporary, Safe, Local):
In PowerShell as Administrator, run:
```

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Then confirm with Y when prompted.



## Python will utilize this requirements.txt in the project:

```
psycopg[binary]
psycopg-pool
```

3. Install the libraries: [only necesary to do this one time per environment]

```
pip3 install -r requirements.txt
```

4. create the grocery_activity table:

```
python3 create_tables.py
```

5. load data into the table:

```
python3 loadgrocerytable.py
```

6. Test the performance:
```
python3 groceryqueries.py
```

7. to open a sql interface: NB: the dbname should match the one you specified in the 
connection_stuff.py file imported by private_stuff.py 

```
cockroach sql --insecure --port 29004
```
