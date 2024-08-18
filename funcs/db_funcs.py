import os
import psycopg2
import hashlib

# Function to make md5 hash
def make_md5_hash(s):
    return hashlib.md5(s.encode()).hexdigest()

# Function to get connection and cursor to database
def get_conn_cur():

    # Get database credentials
    db_cred = {}
    db_cred['ip'] = os.getenv('DB_IP')
    db_cred['db'] = os.getenv('DB_NAME')
    db_cred['user'] = os.getenv('DB_USER')
    db_cred['password'] = os.getenv('DB_PW')
       

    print(db_cred)
    # Connect to database
    conn = psycopg2.connect(
        host=db_cred['ip'],
        database=db_cred['db'],
        user=db_cred['user'],
        password=db_cred['password']
    )
    cur = conn.cursor()

    return conn, cur

# Function to make database entry for LLM response
def make_run_db_entry(d):

# Get database connection and cursor 
    conn, cur = get_conn_cur()

# Format keys,value and query for insertion
    values = ', '.join(['%s'] * len(d))
    keys = ', '.join(d.keys())
    q = f"""INSERT INTO protol_gen_runs_overview ({keys},last_modified) VALUES ({values},now()) RETURNING pool_id"""
   
# Execute query
    cur.execute(q, tuple(d.values()))
    
# Get pool_id
    pool_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    
    return pool_id

# Function to make database entry for LLM output
def make_output_db_entry(project,output,pool_id,mdl):

    # Get database connection and cursor 
    conn,cur = get_conn_cur()

    # Format query for insertion
    q = f"""INSERT INTO {project} (model, output, pool_id,last_modified) VALUES (%s, %s, %s,now())"""
    
    # Execute query
    cur.execute(q, (mdl,output,pool_id))
    
    conn.commit()
    cur.close()
    conn.close()
    return None
