from connection_stuff import *
# note that the details for your connections to the database and LLM etc, will be found in the file connection_stuff.py
# by storing this info in a separate file and including that file in the .gitignore file there is less security risk
# connection_stuff.py will look like this 
'''
# import driver for CRDB/postgres:
import psycopg 
from psycopg_pool import ConnectionPool
import os

### LLM / AI Setup ###
# Q: where is the LLM library? A: we are using a hosted 'localAI' server
# https://localai.io/ 
llm_chat_url = "http://localhost:6060/v1/chat/completions"

### CRDB connection setup ###
# Q: whare is the database? A: we assume a locally hosted insecure CRDB instance

db_url="postgresql://root@localhost:29004/contexte" #/grocery

# to utilize certs set the env variable SECURE_CRDB=true
# SECURE_CRDB=true
CERTDIR = '/Users/owentaylor/.cockroach-certs'
db_config_secure = {
    'host': 'localhost',
    'port': 26257,
    'dbname': 'vdb',
    'user': 'root',
    # SSL parameters:
    'sslmode': 'verify-full',         # or 'verify-full' if your host matches the cert SAN
    'sslrootcert': f'{CERTDIR}/ca.crt',
    'sslcert': f'{CERTDIR}/client.root.crt',
    'sslkey': f'{CERTDIR}/client.root.key',
    'connect_timeout': 10,
}

CERTDIR = f"{os.environ['HOME']}/Library/CockroachCloud/certs/regionaloutagedemo"
db_config_secure = {
    'host': 'regional-outage-demo-vmf.ads-us-west.cockroachlabz.cloud',
    'port': 26257,
    'dbname': 'vdb',
    'user': 'disruptor',
    'password': '9l5UioSG1GoA2ssw2aaS3-Ln-3-w',        # SSL parameters:
    'sslmode': 'verify-full',         # or 'verify-full' if your host matches the cert SAN
    'sslrootcert': f'{CERTDIR}/regional-outage-demo-ca.crt',
    'connect_timeout': 10,
}

# here is where we test for the env variable SECURE_CRDB :
# Initialize pool as None so it persists between function calls
_pool = None

def get_connection():
    global _pool
    if _pool is None:
        if(os.getenv("SECURE_CRDB", "false")=='true'):
            print('GETTING SECURE CONNECTION...')
            _pool = ConnectionPool(conninfo="",**db_config_secure)
        else:
            print('GETTING NON-SECURE (PLAIN) CONNECTION...')
            _pool = ConnectionPool(conninfo=db_url)
        # use unpacking operator ** to turn dict to separate args:
    connection = _pool.connection() 
        
    assert connection is not None, "get_connection() returned None (connection failed)"
    return connection
'''