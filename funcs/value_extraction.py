value_examples = {"temperature": "37.0, 37.0, 37.0, 37.5",
                  "ph": "7.0, 7.0, 7.0, 7.5",
                  "dissolved_oxygen": "5.0, 5.0, 15.0, 5.5",
                  "rpm/impeller speed": "0, 20, 0, 150"}

placeholder_param_extraction_prompt = """Given the following table of %no_of_days, extract the values from the %param column
 and return them as a list of floating-point numbers: \n\n%output\n\nYour task is to extract the %param values and return
   them as a list of numbers. For example, your result should be in the format: %val_example.
     DO NOT PROVDE ANY ADDITIONAL INFORMATION, Just give me the list of %param for each of the %no_of_days days in the table. 
     What is the list of %param?"""


placeholder_compound_extraction_prompt  = """Given the following table, extract the compound(s) used for each day along with their concentrations and units. Return the output as a dictionary of dictionaries, where the keys are the day numbers and the values are dictionaries containing compound names as keys and their corresponding concentrations and units as values. Use the following format:
{
    0: {"Compound 1": {100: "ng/mL"}, "Compound 2": {50: "ng/mL"}},
    1: {"Compound 1": {150: "ng/mL"}, "Compound 3": {20: "ng/mL"}},
    ...
}
Here is the table:\n\n%output\n\n

Note: for days with no concentraion or amount please write None. Write the numbers EXACTLY as they appear in the table, DO NOT FORMAT them in any way """