import os
import psycopg2
import hashlib
import os
import psycopg2

# Function to make md5 hash
def make_md5_hash(s):
    return hashlib.md5(s.encode()).hexdigest()

# Function to get connection and cursor to database
def get_conn_cur():

    # Connect to database
    conn = psycopg2.connect(
        host=os.getenv('DB_IP'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PW'),
        port=os.getenv('DB_PORT')
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

    # Format query for insertion and returning sim_id
    q = f"""
    INSERT INTO {project} (model, output, pool_id,last_modified)
    VALUES (%s, %s, %s,now())
    RETURNING sim_id
    """
    
    cur.execute(q, (mdl,output,pool_id))

    # Get sim_id
    sim_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return sim_id


# Function to update database entry for sim_id for extracted values in dict d
def make_params_db_entry(project, sim_id, param_values):
    # Get database connection and cursor
    conn, cur = get_conn_cur()
    
    # Prepare query and execute
    placeholders = ', '.join([f"{k} = %s" for k in param_values])
    query = f"UPDATE {project} SET {placeholders}, last_modified = now() WHERE sim_id = %s"
    cur.execute(query, (*param_values.values(), sim_id))
    
    # Commit and close
    conn.commit()
    cur.close()
    conn.close()

