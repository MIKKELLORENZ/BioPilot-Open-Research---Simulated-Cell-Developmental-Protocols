import os,re,ast, json

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Move to dir
os.chdir(script_dir)

from ollama import Client
from funcs.db_funcs import make_md5_hash
from funcs.db_funcs import make_run_db_entry
from funcs.db_funcs import make_output_db_entry
from funcs.db_funcs import make_params_db_entry
from funcs.value_extraction import *


# Set up the client
client = Client(host='http://192.168.1.11:11434')
# UNCOMMENT THE LINE BELOW TO USE LOCALHOST
#client = Client(host='http://localhos:11434')


no_of_days = 21

# Read prompt from prompts folder
prompt = open(script_dir + "/prompts/liver_organoids_1.txt", "r").read()

# number of protocols to generate
no_protocols_per_model = 10000

# Which models to use for protocol generation
models = ['llama3.1:8b', 'gemma2', 'mistral-nemo']

# List which environmental parameters to extract
env_parameters = ["temp", "ph", "dissolved_oxygen", "rpm"]

# Format prompt
prompt = prompt.replace("%no_of_days", str(no_of_days))

# Set data for database entry
d = {}
d["project"] = "simulated_cell_developmental_protocols"
d["prompt_md5_hash"] = make_md5_hash(prompt)
d["product"] = "liver_organoids"
d["no_of_days"] = no_of_days
# Make database entry for current run
 
pool_id = make_run_db_entry(d)

## Print statement with parameters
print("Starting protocol generation for", d["product"], "with prompt", d["prompt_md5_hash"][:100]+"...")
# Main loop to generate protocols
for mdl in models:
    for i in range(no_protocols_per_model):
        print("_________________________________________________")
        print("Generating protocol", i+1, "using model", mdl)
        response = client.chat(model=mdl, messages=[
        {'role': 'user',
        'content': f'{prompt}'}],
        options={"stop":[f"| {no_of_days+1}  |"]}
        )

# Get output from response
        output = response["message"]["content"]

        print("Response is:\n", output)
# Make database entry for current output
        sim_id = make_output_db_entry(d["project"],output,pool_id,mdl)
        print("Sim_id is:", sim_id,"\n")

# Dict for storing extracted values
        param_values = {}

# Perform value extraction
        formatted_output = output.replace("C","").replace("°","").replace("]","").replace("[","").replace("%","")
        for param in env_parameters:
                print("\n Parameter is:", param)
                extraction = re_extraction(param,formatted_output)

                print("FOUND VALUES")
                print(param_values)
                param_values[param.split("/",2)[0].replace("temp","temperature")] =  extraction
                print("__________________")
# Extract compounds and amounts
        compound_extraction = placeholder_compound_extraction_prompt.replace("%output", output)
        compound_extraction_response = client.chat(model=mdl, messages=[
        {'role': 'user',
        'content': f'{compound_extraction}'}])

        compound_extraction_response = compound_extraction_response["message"]["content"]

        print(compound_extraction_response)

        # Convert string to dictionary
        try:
                param_values["compounds"] = json.dumps(ast.literal_eval(compound_extraction_response))
        except Exception as e:
                print("Could not convert to dictionary. Error is ", e)
                param_values["compounds"] =  {}

# Finally insert the extracted values into the database
        try:    
                print("Attempting to insert extracted values into database for sim_id:", sim_id)
                make_params_db_entry(d["project"], sim_id, param_values)
                print("Success")
        except Exception as e:
                print(f"Could not insert extracted values into database for sim_id {sim_id}. Error is ", e)


