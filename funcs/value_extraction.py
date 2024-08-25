import re

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