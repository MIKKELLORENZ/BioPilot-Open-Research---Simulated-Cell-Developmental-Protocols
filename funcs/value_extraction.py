import re

placeholder_compound_extraction_prompt = """
Given the following table, extract the compound(s) used for each day along with their concentrations and units. Return the output as a dictionary of dictionaries, where the keys are the day numbers and the values are dictionaries containing compound names as keys and their corresponding concentrations and units as values. Use the following format:

{
    0: {"Compound 1": {100: "ng/mL"}, "Compound 2": {50: "ng/mL"}},
    1: {"Compound 1": {150: "ng/mL"}, "Compound 3": {20: "ng/mL"}},
    ...
}
Where Compounds are the real compounds names and concentrations are the numerical values with units.

Here is the table:

%output

Important instructions:
1. For days with no concentration or amount, use None (Python's None object, not a string) for both concentration and unit.
2. Write numbers EXACTLY as they appear in the table without any formatting changes.
3. Only consider the compound column for extraction. Ignore patterns like (100x) and use None for both concentration and unit in such cases.
4. If a compound has multiple concentrations on the same day, list them as separate entries.
5. If units are missing but a concentration is given, use None for the unit.
6. Ensure all day numbers are integers.

What are the compounds and their concentrations for each day? Provide only the final dictionary without any additional comments.
"""


def re_extraction(param,text):

    lines = text.strip().split('\n')

    for i,line in enumerate(lines):
      if "|" in line:
          break
      
    lines = lines[i:]

    # Strip whitespace from headers and convert to lowercase
    headers = [header.lower().replace(" ","_") for header in lines[0].split('|')]

    for header in headers:
        if param.lower() in header:
            param_index = headers.index(header)
            break
      
    if "compound" in param.lower():
        values = {}
    else:
        values = []

    # Extract the values from the identified column
    for line in lines[2:]:  # Skip the header and separator lines
 
        columns = line.split('|')
        if len(columns) > 2:
          
          if "temp" in param.lower():
              column_value = columns[param_index].replace("C","").replace("c","").strip()

          elif "rpm" in param.lower():
              column_value = columns[param_index].replace("RPM","").replace("rpm","").strip()         

          else:
              column_value = columns[param_index].strip()
              day = columns[0].strip()

          if "compound" not in param.lower():

            if type(column_value) == None:
                values.append(None)
            elif len(column_value) > 0:
                values.append(float(column_value))

          else:
            values[day] = column_value
          
    return values