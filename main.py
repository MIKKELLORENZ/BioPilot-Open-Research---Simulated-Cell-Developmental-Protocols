import os
from ollama import Client
from funcs.db_funcs import make_md5_hash
from funcs.db_funcs import make_run_db_entry
from funcs.db_funcs import make_output_db_entry

# Set up the client
client = Client(host='http://192.168.1.11:11434')

# Read prompt from prompts folder
prompt = open("prompts/liver_organoids_1.txt", "r").read()

# Set model to use in generating response
model = 'llama3.1:8b' # 8b model

# number of protocols to generate
no_protocols_per_model = 5

# Which models to use
models = ['llama3.1:8b', 'gemma2', 'mistral-nemo']

# Set data for database entry
d = {}
d["project"] = "simulated_cell_development_protocols"
d["prompt_md5_hash"] = make_md5_hash(prompt)
d["product"] = "liver_organoids"

# Make database entry for current run
pool_id = make_run_db_entry(d)

# Main loop to generate protocols
for mdl in models:
    for i in range(no_protocols_per_model):
        print("Generating protocol", i+1, "for model", mdl)
        response = client.chat(model=mdl, messages=[
        {
            'role': 'user',
            'content': f'{prompt}',
        },
        ])

# Get output from response
        output = response["message"]["content"]


# Make database entry for current output
        make_output_db_entry(d["project"],output,pool_id,mdl)


