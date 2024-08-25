import re

value_examples = {"paramerature": "37.0, 37.0, 37.0, 37.5",
                  "ph": "7.0, 7.0, 7.0, 7.5",
                  "dissolved_oxygen": "5.0, 5.0, 15.0, 5.5",
                  "rpm/impeller speed": "0, 20, 0, 150"}

# placeholder_param_extraction_prompt = """Given the following table of %no_of_days, extract the values from the %param column
#  and return them as a list of floating-point numbers: \n\n%output\n\nYour task is to extract the %param values and return
#    them as a list of numbers. For example, your result should be in the format: %val_example.
#      DO NOT PROVDE ANY ADDITIONAL INFORMATION, Just give me the list of %param for each of the rows in the table. 
#      IMPORTANT: Look twice and carefully. ONLY if a particular row has no value for %param should you write 'None' in that SPECIFIC element positions. Think deeply and DO NOT OVER DO it. The list must of course add up to the length of %no_of_days_plus_1 (because we are inclduing including day 0). What is the precise list of %param?"""

placeholder_param_extraction_prompt = """Given the following table of %no_of_days, extract the values from the %param column and return them as a list of floating-point numbers. Your task is to extract the %param values and return them as a list of numbers. For example, your result should be in the format: %val_example. 

DO NOT PROVIDE ANY ADDITIONAL INFORMATION. Just give me the list of %param for each of the rows in the table. IMPORTANT: Carefully verify each row. The final list must match the length of %no_of_days_plus_1 (because we are including day 0). What is the precise list of %param?: \n\n%output\n\n"""

placeholder_compound_extraction_prompt  = """Given the following table, extract the compound(s) used for each day along with their concentrations and units. Return the output as a dictionary of dictionaries, where the keys are the day numbers and the values are dictionaries containing compound names as keys and their corresponding concentrations and units as values. Use the following format:
{
    0: {"Compound 1": {100: "ng/mL"}, "Compound 2": {50: "ng/mL"}},
    1: {"Compound 1": {150: "ng/mL"}, "Compound 3": {20: "ng/mL"}},
    ...
}
Here is the table:\n\n%output\n\n

Note: for days with no concentraion or amount please write None. 
Write the numbers EXACTLY as they appear in the table and DO NOT FORMAT them in any way. 
ONLY consider the compound column. If you encounter patterns  like (100x) you should simply write None. 
What are the compounds and their concentrations for each day? Give me the final dictionary with no additional comments. """


def re_extraction(param,text):

    lines = text.strip().split('\n')
    print("ALL LINES ARE:")
    for line in lines:
        print(line)

    for i,line in enumerate(lines):
      if "|" in line:
          break
      
    lines = lines[i:]

    # Strip whitespace from headers and convert to lowercase
    headers = [header.lower().replace(" ","_") for header in lines[0].split('|')]

    print("Headers are:", headers)

    for header in headers:
        if param.lower() in header:
            param_index = headers.index(header)
            break
      
    values = []
    print("Parameter index is:", param_index)

    # Extract the values from the identified column
    for line in lines[2:]:  # Skip the header and separator lines
 
        columns = line.split('|')
        if len(columns) > 2:
          
          column_value = columns[param_index].replace("RPM","").replace("rpm","").strip()
        # print("COLUM VALUE FOUDN IS:", column_value)
          if type(column_value) == None:
              values.append(None)
          elif len(column_value) > 0:
              values.append(float(column_value))
    
    return values