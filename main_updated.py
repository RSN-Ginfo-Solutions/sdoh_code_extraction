from bluebuttonpy import CCDA
import os
import re
import pandas as pd
from tqdm import tqdm

import re
import os
import time
from litellm import completion
from litellm import token_counter

# from together import Together
# client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

def process_ccda(file_path):
  with open(file_path) as f: 
    ccd = CCDA(f.read())
    data = ccd.data 
    d = dict()
  
  #DEMOGRAPHICS
  demographics_info = (
    f"{data.demographics.name.given} {data.demographics.name.family} "
    f"{data.demographics.gender} "
    f"{data.demographics.marital_status} {data.demographics.address.city} "
    f"{data.demographics.email} "
    f"{data.demographics.language} {data.demographics.race} "
    f"{data.demographics.ethnicity} {data.demographics.religion} "
    f"{data.demographics.birthplace.state}"
    f"{data.demographics.birthplace.country} {data.demographics.guardian.name.given} "
    f"{data.demographics.guardian.name.family} {data.demographics.guardian.relationship} "
    f"{data.demographics.provider.organization}" 
    )
  d["demographics_info"] = demographics_info
 
 #"{data.demographics.dob} {data.demographics.provider.phone} {data.demographics.guardian.relationship_code}
 #{data.demographics.phone.mobile} {data.demographics.birthplace.zip} 
 # f"{data.demographics.phone.home} {data.demographics.phone.work} "
 #f"{data.demographics.guardian.phone.home} "

  #ALLERGIES
  allergies_info = ""
  for allergy in data.allergies:
    allergies_info += (
      f"{allergy.name}"
      f"{allergy.status} {allergy.severity} "
      f"{allergy.reaction.name} {allergy.reaction_type.name}"
      f"{allergy.allergen.name}")
  
  d["allergies_info"] = allergies_info

#{allergy.date_range.start} {allergy.date_range.end}
#{allergy.code} {allergy.code_system} {allergy.code_system_name} {allergy.reaction.code} 
#{allergy.reaction.code} {allergy.reaction.code_system} {allergy.reaction_type.code}
#{allergy.reaction_type.code_system} {allergy.reaction_type.code_system_name}  {allergy.allergen.code} 
#{allergy.allergen.code_system} {allergy.allergen.code_system_name} 


  #DOCUMENT
  # document_info = (
  # f"{data.document.date} {data.document.title} "
  # f"{data.document.author.name.given} {data.document.author.name.family} "
  # f"{data.document.author.address.city} {data.document.author.phone.work} "
  # f"{data.document.location.name} {data.document.location.address.city} "
  # f"{data.document.location.encounter_date} ")

  # d["document_info"] = document_info

  #ENCOUNTERS
  encounters_info = ""
  for entry in data.encounters:
    encounters_info += (f"{entry.name} {entry.translation.name} {entry.performer.name}" )
      # f"{entry.name}"
      # f"{entry.code_system_name} {entry.code_system_version} "
      # f"{entry.translation.name} {entry.translation.code} "
      # f"{entry.translation.code_system} {entry.translation.code_system_name} "
      # f"{entry.performer.name} {entry.performer.code} "
      # f"{entry.performer.code_system} {entry.performer.code_system_name} ")
  
  for finding in entry.findings:
      encounters_info += (
          f"{finding.name}")
  
  d["encounters_info"] = encounters_info

#{entry.code} {entry.code_system} 
#{finding.code} {finding.code_system} 

  #FUNCTIONAL STATUSES
  functional_statuses_info = ""
  for entry in data.functional_statuses:
    functional_statuses_info += (
      f"{entry.name}")
  
  d["functional_statuses_info"] = functional_statuses_info

#{entry.date}{entry.code} {entry.code_system} {entry.code_system_name}  

  #IMMUNIZATIONS
  immunizations_info = ""
  for entry in data.immunizations:
    immunizations_info += (
        f"{entry.product.name} {entry.product.translation.name} {entry.route.name}")
        # f"{entry.product.translation.name} {entry.product.translation.code} "
        # f"{entry.product.translation.code_system} {entry.product.translation.code_system_name} "
        # f"{entry.product.lot_number} {entry.product.manufacturer_name} "
        # f"{entry.dose_quantity.value} {entry.dose_quantity.unit} "
        # f"{entry.route.name} {entry.route.code} {entry.route.code_system} "
        # f"{entry.route.code_system_name} {entry.instructions} "
        # f"{entry.education_type.name} {entry.education_type.code} "
        # f"{entry.education_type.code_system} ")
  
  d["immunizations_info"] = immunizations_info

#{entry.date} {entry.product.code}
#f"{entry.product.code_system} {entry.product.code_system_name} "


  #INSTRUCTIONS
  instructions_info = ""
  for entry in data.instructions:
    instructions_info += (
      f"{entry.text} {entry.name}") # {entry.code} "
      #f"{entry.code_system} {entry.code_system_name} ")
  d["instructions_info"] = instructions_info

  #MEDICATIONS
  medications_info = ""
  for entry in data.medications:
    medications_info += (
      f"{entry.text} "
      f"{entry.product.name}"
      f"{entry.product.text} {entry.product.translation.name} "
      f"{entry.precondition.name}"
      f"{entry.reason.name}"
      f"{entry.route.name}"
      f"{entry.administration.name}"
      f"{entry.prescriber.organization} {entry.prescriber.person} "
  )
  d["medications_info"] = medications_info

#{entry.date_range.start} {entry.date_range.end}
#f"{entry.product.translation.code} {entry.product.translation.code_system} "
#{entry.dose_quantity.value} {entry.product.code} {entry.product.code_system}
#f"{entry.dose_quantity.unit} {entry.rate_quantity.value} {entry.rate_quantity.unit} "
#{entry.precondition.code} {entry.precondition.code_system} {entry.product.translation.code_system_name}
#{entry.reason.code} {entry.reason.code_system} 
#{entry.route.code} {entry.route.code_system}
#f"{entry.route.code_system_name} {entry.schedule.type} {entry.schedule.period_value} "
#f"{entry.schedule.period_unit} {entry.vehicle.name} {entry.vehicle.code} "
#f"{entry.vehicle.code_system} {entry.vehicle.code_system_name} "
#{entry.administration.code} 
#f"{entry.administration.code_system} {entry.administration.code_system_name} "



  #PROBLEMS
  problems_info = ""
  for entry in data.problems:
    problems_info += (f"{entry.name} {entry.age} {entry.translation.name} {entry.comment}")
      # f"{entry.date_range.start} {entry.date_range.end} "
      # f"{entry.status} {entry.code} {entry.code_system} "
      # f"{entry.code_system_name} "
      # f"{entry.translation.code} {entry.translation.code_system} "
      # f"{entry.translation.code_system_name}")
  
  d["problems_info"] = problems_info

  #PROCEDURES
  procedures_info = ""
  for entry in data.procedures:
    procedures_info += (f"{entry.name} {entry.specimen.name} {entry.device.name}")
      # f"{entry.date} {entry.name} {entry.code} {entry.code_system} "
      # f"{entry.specimen.name} {entry.specimen.code} {entry.specimen.code_system} "
      # f"{entry.device.name} {entry.device.code} {entry.device.code_system} "
      # f"{entry.performer.phone} ")
  
  d["procedures_info"] = procedures_info

  #RESULTS
  lab_test_results_info = ""
  for entry in data.results:
    for test in entry.tests:
      lab_test_results_info += (f"{entry.name} {test.name} {test.translation.name}")
      #     f"{entry.name} {entry.code} {entry.code_system} {entry.code_system_name} "
      #     f"{test.date} {test.name} {test.code} {test.code_system} {test.code_system_name} "
      #     f"{test.value} {test.unit} {test.translation.name} {test.translation.code} "
      #     f"{test.translation.code_system} {test.translation.code_system_name} "
      #     f"{test.reference_range.low_unit} {test.reference_range.low_value} "
      #     f"{test.reference_range.high_unit} {test.reference_range.high_value} "
      # )

  d["lab_test_results_info"] = lab_test_results_info

  #SOCIAL HISTORY
  sdoh_info=""
  temp_sdoh = data.smoking_status
  for entry in temp_sdoh:
    sdoh_info+= (f"{entry.name}, ")
  d["social_history_info"]=sdoh_info

#{entry.code} {entry.code_system} {entry.code_system_name}


  #VITALS
  temp_vit = data.vitals
  vitals_info = ""
  for entry in temp_vit:
    for result in entry.results:
      vitals_info += f"{result.name} {result.value} {result.unit}"
  d["vitals_info"] = vitals_info
#f"{entry.date} {result.name} {result.code} {result.code_system} {result.code_system_name} {result.value} {result.unit} "
  
  dict_string = ' '.join([f"'{key}': '{value}'" for key, value in d.items()])
  # print(f"Dict string:{dict_string}")
  cleaned_text = re.sub(r"[\[\]']", '', dict_string)
  cleaned_text = cleaned_text.replace('None','')
  cleaned_text = ' '.join(cleaned_text.split())
  # print(f"Cleaned text: {cleaned_text}")
  return cleaned_text

# output = process_ccda('/content/Patient-289.xml')
# print(output)

def social_code_extraction(input_text):
    # Prepare all categories and codes at once
    all_codes = """
    
    Risk Factor - Code
    Illiteracy and low-level literacy - Z55.0
    Schooling unavailable and unattainable - Z55.1
    Failed school examinations - Z55.2
    Underachievement in school - Z55.3
    Educational maladjustment and discord with teachers and classmates - Z55.4
    Less than a high school diploma - Z55.5
    Problems related to health literacy - Z55.6
    Other problems related to education and literacy - Z55.8
    Problems related to education and literacy, unspecified - Z55.9

    Unemployment, unspecified - Z56.0
    Change of job - Z56.1
    Threat of job loss - Z56.2
    Stressful work schedule - Z56.3
    Discord with boss and workmates - Z56.4
    Uncongenial work environment - Z56.5
    Other physical and mental strain related to work - Z56.6
    Other problems related to employment - Z56.8
    Sexual harassment on the job - Z56.81
    Military deployment status - Z56.82
    Other problems related to employment - Z56.89
    Unspecified problems related to employment - Z56.9

    Occupational exposure to noise - Z57.0
    Occupational exposure to radiation - Z57.1
    Occupational exposure to dust - Z57.2
    Occupational exposure to other air contaminants - Z57.3
    Occupational exposure to environmental tobacco smoke - Z57.31
    Occupational exposure to other air contaminants - Z57.39
    Occupational exposure to toxic agents in agriculture - Z57.4
    Occupational exposure to toxic agents in other industries - Z57.5
    Occupational exposure to extreme temperature - Z57.6
    Occupational exposure to vibration - Z57.7
    Occupational exposure to other risk factors - Z57.8
    Occupational exposure to unspecified risk factor - Z57.9

    Inadequate drinking-water supply - Z58.6
    Other problems related to physical environment - Z58.8
    Basic services unavailable in physical environment - Z58.81
    Other problems related to physical environment - Z58.89

    Homelessness - Z59.0
    Homelessness unspecified - Z59.00
    Sheltered homelessness - Z59.01
    Unsheltered homelessness - Z59.02
    Inadequate housing - Z59.1
    Inadequate housing, unspecified - Z59.10
    Inadequate housing environmental temperature - Z59.11
    Inadequate housing utilities - Z59.12
    Other inadequate housing - Z59.19
    Discord with neighbors, lodgers and landlord - Z59.2
    Problems related to living in residential institution - Z59.3
    Lack of adequate food - Z59.4
    Food insecurity - Z59.41
    Other specified lack of adequate food - Z59.48
    Extreme poverty - Z59.5
    Low income - Z59.6
    Insufficient social insurance and welfare support - Z59.7
    Other problems related to housing and economic circumstances - Z59.8
    Housing instability, housed - Z59.81
    Housing instability, housed, with risk of homelessness - Z59.811
    Housing instability, housed, homelessness in past 12 months - Z59.812
    Housing instability, housed unspecified - Z59.819
    Transportation insecurity - Z59.82
    Financial insecurity - Z59.86
    Material hardship due to limited financial resources, not elsewhere classified - Z59.87
    Other problems related to housing and economic circumstances - Z59.89
    Problem related to housing and economic circumstances, unspecified - Z59.9

    Problems of adjustment to life-cycle transitions - Z60.0
    Problems related to living alone - Z60.2
    Acculturation difficulty - Z60.3
    Social exclusion and rejection - Z60.4
    Target of (perceived) adverse discrimination and persecution - Z60.5
    Other problems related to social environment - Z60.8
    Problem related to social environment, unspecified - Z60.9

    Inadequate Parental Supervision and Control - Z62.0
    Parental Overprotection - Z62.1
    Upbringing Away from Parents - Z62.2
    Child in Welfare Custody - Z62.21
    Institutional Upbringing - Z62.22
    Child in Custody of Non-Parental Relative - Z62.23
    Child in Custody of Non-Relative Guardian - Z62.24
    Other Upbringing Away from Parents - Z62.29
    Hostility Towards and Scapegoating of Child - Z62.3
    Inappropriate (Excessive) Parental Pressure - Z62.6
    Other Specified Problems Related to Upbringing - Z62.8
    Personal History of Abuse in Childhood - Z62.81
    Personal History of Physical and Sexual Abuse in Childhood - Z62.810
    Personal History of Psychological Abuse in Childhood - Z62.811
    Personal History of Neglect in Childhood - Z62.812
    Personal History of Forced Labor or Sexual Exploitation in Childhood - Z62.813
    Personal History of Child Financial Abuse - Z62.814
    Personal History of Intimate Partner Abuse in Childhood - Z62.815
    Personal History of Unspecified Abuse in Childhood - Z62.819
    Parent-Child Conflict - Z62.82
    Parent-Biological Child Conflict - Z62.820
    Parent-Adopted Child Conflict - Z62.821
    Parent-Foster Child Conflict - Z62.822
    Parent-Step Child Conflict - Z62.823
    Non-Parental Relative or Guardian-Child Conflict - Z62.83
    Non-Parental Relative-Child Conflict - Z62.831
    Non-Relative Guardian-Child Conflict - Z62.832
    Group Home Staff-Child Conflict - Z62.833
    Other Specified Problems Related to Upbringing - Z62.89
    Parent-Child Estrangement NEC - Z62.890
    Sibling Rivalry - Z62.891
    Runaway [From Current Living Environment] - Z62.892
    Other Specified Problems Related to Upbringing - Z62.898
    Problem Related to Upbringing, Unspecified - Z62.9

    Problems in Relationship with Spouse or Partner - Z63.0
    Problems in Relationship with In-Laws - Z63.1
    Absence of Family Member - Z63.3
    Due to Military Deployment - Z63.31
    Other Absence of Family Member - Z63.32
    Disappearance and Death of Family Member - Z63.4
    Disruption of Family by Separation and Divorce - Z63.5
    Dependent Relative Needing Care at Home - Z63.6
    Other Stressful Life Events Affecting Family and Household - Z63.7
    Stress on Family Due to Return of Family Member from Military Deployment - Z63.71
    Alcoholism and Drug Addiction in Family - Z63.72
    Other Stressful Life Events Affecting Family and Household - Z63.79
    Other Specified Problems Related to Primary Support Group - Z63.8
    Problem Related to Primary Support Group, Unspecified - Z63.9

    Problems Related to Unwanted Pregnancy - Z64.0
    Problems Related to Multiparity - Z64.1
    Discord with Counselors - Z64.4
    Problems Related to Other Psychosocial Circumstances - Z65
    Conviction in Civil and Criminal Proceedings Without Imprisonment - Z65.0
    Imprisonment and Other Incarceration - Z65.1
    Problems Related to Release from Prison - Z65.2
    Problems Related to Other Legal Circumstances - Z65.3
    Victim of Crime and Terrorism - Z65.4
    Exposure to Disaster, War, and Other Hostilities - Z65.5
    Other Specified Problems Related to Psychosocial Circumstances - Z65.8
    Problem Related to Unspecified Psychosocial Circumstances - Z65.9
    """
    prompt = f"""
      Following is a list of possible social determinants of health factors and their corresponding codes:
      {all_codes}
      Your task is to identify any of the factors if present in the given text and return the correct
      corresponding code for the identified factor.

      Input Text: {input_text}

      Instructions:
      1.Carefully read the input text and identify if any of the mentioned factors are present.
      2.For any identified piece of text, find the corresponding code as listed above.
      3.Only Return the identified piece of text and its corresponding factor and associated code in the following format:
        [identified text : factor : code].
      4. Only return the output of Point 3, nothing else, no extra text, no python code,no comments or explanations.
      5. If no factor is found, just say-"No SDOH factor found".
      """  
########LITE LLM
    #groq/llama-3.1-8b-instant
    model= "groq/llama-3.1-8b-instant" #"groq/llama-3.1-70b-versatile" 
    messages = [{"role": "user", "content": prompt}]
    # input_token_count = token_counter(model=model, messages=messages)
    
    #call responses for Groq via litellm
    response = completion(
        model=model,
        messages=messages,
        temperature=0
    )
    result = response['choices'][0]['message']['content'] or ""

    # # Call Together AI to get the LLM response
    # stream = client.chat.completions.create(
    #     model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
    #     messages=messages,
    #     stream=False,)
    # # Collect the response content
    # result = ""
    # for chunk in stream:
    #     result += chunk.choices[0].delta.content or ""
 
    # print(f"Resultant codes: {result}")
    return result
    # cleaned_text = '\n'.join(line for line in result.splitlines() if line != "Here is the output:")
    # return cleaned_text
  
#####Testing- Code to run for single file
#process_ccda('/content/Patient-102.xml')
#('/content/xml_repo/EMERGE/Patient-263.xml') 
output1 = process_ccda('/content/Patient-10.xml')
print(f"Extracted Text: {output1}")
output2 = social_code_extraction(output1)
print(f"Extracted codes: {output2}")

######Code to run for ALL files with continuous updates

# def process_multiple_files(file_paths, output_csv_path):
#     # Initialize an empty DataFrame or load existing one if it already exists
#     if os.path.exists(output_csv_path):
#         new_df = pd.read_csv(output_csv_path)
#     else:
#         new_df = pd.DataFrame(columns=["File Name", "Extracted info", "SDOH codes"])
    
#     failed_files = []

#     # Limit processing to the first 50 files
#     for index, file_path in tqdm(enumerate(file_paths[:50]), total=min(50, len(file_paths)), desc="Extraction of codes"):
#         try:
#             result = process_ccda(file_path)
#             sdoh_info = social_code_extraction_gradio(result)
#             file_name = os.path.basename(file_path)
#             new_entry = pd.DataFrame({
#                 "File Name": [file_name],
#                 "Extracted info": [result],
#                 "SDOH codes": [sdoh_info]
#             })
#             # Append new entry to the DataFrame and save to CSV
#             new_df = pd.concat([new_df, new_entry], ignore_index=True)
#             new_df.to_csv(output_csv_path, index=False)  # Update CSV file

#         except Exception as e:
#             file_name = os.path.basename(file_path)
#             error_message = str(e)
#             failed_files.append((file_name, error_message))
#             with open("failed_files.txt", "a") as f:  # Use 'a' to append to the file
#                 f.write(f"File: {file_name} - Error: {error_message}\n")

#     return new_df, failed_files

# file_dir = '/content/xml_repo/EMERGE'
# file_paths = [os.path.join(file_dir, filename) for filename in os.listdir(file_dir) if filename.endswith('.xml')]
# output_csv_path = '/content/results/extracted_sdoh_info_final.csv'

# df, failed_files_list = process_multiple_files(file_paths, output_csv_path)
# print(df.shape)


