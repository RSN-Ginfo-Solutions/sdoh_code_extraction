from bluebuttonpy.core import wrappers
from bluebuttonpy.parsers.ccda.allergies import allergies
from bluebuttonpy.parsers.ccda.care_plan import care_plan
from bluebuttonpy.parsers.ccda.demographics import demographics
from bluebuttonpy.parsers.ccda.document import document
from bluebuttonpy.parsers.ccda.encounters import encounters
from bluebuttonpy.parsers.ccda.free_text import free_text
from bluebuttonpy.parsers.ccda.functional_statuses import functional_statuses
from bluebuttonpy.parsers.ccda.immunizations import immunizations
from bluebuttonpy.parsers.ccda.instructions import instructions
from bluebuttonpy.parsers.ccda.medications import medications
from bluebuttonpy.parsers.ccda.problems import problems
from bluebuttonpy.parsers.ccda.procedures import procedures
from bluebuttonpy.parsers.ccda.results import results
from bluebuttonpy.parsers.ccda.smoking_status import smoking_status
from bluebuttonpy.parsers.ccda.vitals import vitals

"""
Created on Mon Jul  2 21:36:34 2018

@author: mansooralam, yanjingwang

Modified on Jul 26, 2024:

@author: srikanth235
"""


def run(ccda):
    data = wrappers.ObjectWrapper()

    data.document = document(ccda)
    data.allergies = allergies(ccda)
    data.care_plan = care_plan(ccda)
    data.chief_complaint = free_text(ccda, 'chief_complaint')
    data.demographics = demographics(ccda)
    data.encounters = encounters(ccda)
    data.functional_statuses = functional_statuses(ccda)
    data.immunizations = immunizations(ccda).administered
    data.immunization_declines = immunizations(ccda).declined
    data.instructions = instructions(ccda)
    data.results = results(ccda)
    data.medications = medications(ccda)
    data.problems = problems(ccda)
    data.procedures = procedures(ccda)
    data.smoking_status = smoking_status(ccda)
    data.vitals = vitals(ccda)

    return data
