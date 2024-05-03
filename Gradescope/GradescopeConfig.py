# EVERYTHING HERE CAN BE CHANGED, JUST READ THE DESCRIPTION BEFORE DOING SO
# GO TO THE BOTTOM WHEN RUNNING THIS SCRIPT

import os
os.chdir(os.path.dirname(__file__))

OUTPUT_DIR = "output/"

############# GRADESCOPE COURSE NUMBER #############
# This comes from the url https://www.gradescope.com/courses/703259
GRADESCOPE_COURSE_NUMBER = 703259

############ CANVAS ROSTER #####################
# export directly from canvas and save the csv in this file system
# This file is intended to be in the parent directoy not in the gradescope folder
CANVAS_ROSTER = "../canvas_roster.csv"

############## PUT ASSIGNMENT NUMBERS HERE AS FOLLOWS #############
####    "Name of assignment" : [assignment ids for each version]
### assignment ids also come from url https://www.gradescope.com/courses/703259/assignments/3989512
BIG_LOOK_UP_TABLE = {
    "Module 1: Quiz": {"all": 3952727},
    "Module 1: Quiz alts": {"alts": 4031687},
    "Module 2: Quiz": {"idk": 4009270, "alts":4031746},  # Already published: 3989512, 4009272  # Joel: not used 4009266 
    "Module 2: Quiz alts": {"alts": 4031746},
    "Module 3: Quiz": {"001":4025219, "003":4025034, "004": 4025220, "005":4025222, "008":4025234, "009":4025236, "006":4025276},
    "Module 4: Exam": {"all": 4065801, "sdc": 4082832, "alts": 4075164},
    "Module 5: Quiz": {"001": 4111118, "003":4111017, "004":4111120, "005":4111123, "006":4111125, "008":4111128, "009":4111130, "alts":4111131},
    "Module 6: Quiz": {"001": 4146608, "003":4142956, "004":4146609, "005":4146610, "006":4146611, "008":4146612, "009":4146613, "alts":4150548},
    "Module 7: Quiz": {"001": 4146634, "003":4178767, "004":4178772, "005":4178773, "006":4178786, "008":4178775, "009":4178776},
    "Module 8: Exam": {"all": 4186348},
    "Module 9: Quiz": {"001": 4258688, "003":4258769, "004":4258771, "005":4258790, "006":4258795, "008":4258800, "009":4258803, "alts":4283270},
    "Module 10: Quiz": {"001": 4283525, "003":4283581, "004":4283583, "005":4283587, "006":4283591, "008":4283593, "009":4283594, "alts":4307877},
    "Module 11: Quiz": {"001": 4318686, "003":4318799, "004":4318800, "005":4318802, "006":4318805, "008":4318808, "009":4318810},
    "Module 12: Exam": {"all": 4349872, "alts1":4384314, "alts2":4384326},
    "Module 13: Quiz": {"001": 4380568, "003":4380622, "004":4380625, "005":4380614, "006":4380628, "008":4380646, "009":4380659, "alts":4399609},
    "Module 14: Quiz": {"001": 4416783, "003":4416670, "004":4416802, "005":4416805, "006":4416807, "008":4416808, "009":4416810},
    "Module 15: Quiz": {"001": 4439599, "003":4439712, "004":4439713, "005":4439715, "006":4439717, "008":4439718, "009":4439719, "alts":4439737},
}

################# THE GRADESCOPE API ##############
## 1) add you grade scope credentials to config.yaml

## grade scope has updated how they export data but the API has not changed
## to fix this. But the following will fix things
## if things break again then this may need to be modified again
## ill write up a bit about how i found this number later
import gradescope  # using API here: https://github.com/mooey5775/gradescope/tree/master
gradescope.util.NUM_HOUSEKEEPING_COLS = 13



########### Rubrics ############
## Change the following depending on how the rubric scores are being use in canvas
## and grade Scope. They must be the same. Do not change the name of RubricScore
## but you can change anything else that makes sense

from enum import Enum
class RubricScore(Enum):
    Satisfactory = "Satisfactory"
    RevisionNeeded = "Minor Revision"
    NotYet = "Not Yet"
    NotGradable = "Not gradable"

default_rubric_eval = RubricScore.NotGradable.value

# This was only for Mod 1 Spring 2024. SO it should be deleted at some point
class RubricScoreMod1(Enum):
    Satisfactory = "Satisfactory (S)"
    RevisionNeeded = "Minor Revision Needed (MR)"
    NotYet = "Not Yet (NY)"
    NotGradable = "Not Gradable (NG)"

# Change depending on how the gradescope rubric is set up
# currently this is looking for a rubric group called "L2 Rubric Score"
# with the options according to RubricScore
def get_standard_rubric_key(standard="", grade=None):
    return f"{standard} Rubric Score: {"" if grade is None else grade}"




###################### RUNNING THIS SCRIPT #################
# Assignment Name to get evals for. This should match the name in
# BIG_LOOK_UP_TABLE made at the top
ASSIGNMENT_NAME = "Module 15: Quiz"
# leave empty to do all sections, or ["001"] do only do section 001
SECTIONS = []  # M13Q: all but 4,6, #M14Q all but 6

# Run the file ExportFromGradescope.py! or run this file. either will work
# good luck!
if __name__ == '__main__': 
    exec(open("ExportFromGradescope.py").read())

# You can upload the output of the file to canvas via tamper monkey
# check out the following:
# https://oit.colorado.edu/services/teaching-learning-applications/canvas/enhancements-integrations/enhancements

