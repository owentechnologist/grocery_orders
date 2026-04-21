## Python-preparation Steps for running the program on your machine:


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

4. to open a sql interface: (remember to then "use grocery" after you connect)

```
cockroach sql --insecure --port 29004
```
