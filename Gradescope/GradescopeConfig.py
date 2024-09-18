# ALMOST EVERYTHING HERE CAN BE CHANGED, JUST READ THE DESCRIPTION BEFORE DOING SO
# GO TO THE BOTTOM WHEN RUNNING THIS SCRIPT

import os
os.chdir(os.path.dirname(__file__))

OUTPUT_DIR = "output/"

############# GRADESCOPE COURSE NUMBER #############
# This comes from the url https://www.gradescope.com/courses/703259
GRADESCOPE_COURSE_NUMBER = 823917

############ CANVAS ROSTER #####################
# export directly from canvas and save the csv in this file system
# This file is intended to be in the parent directoy not in the gradescope folder
CANVAS_ROSTER = "../canvas_roster.csv"

############## PUT ASSIGNMENT NUMBERS HERE AS FOLLOWS #############
####    "Name of assignment" : [assignment ids for each version]
### assignment ids also come from url https://www.gradescope.com/courses/703259/assignments/3989512
BIG_LOOK_UP_TABLE = {
    "Module 1: Quiz": {"001": 4774728, "002": 4774830, "003":4774832, "004":4774833, "006":4774834, "008": 4774841, "009": 4774842, "010":4774844, "012": 4774845, "015": 4774846, "alts":4774880},
    "Module 2: Quiz": {"001": 4837596, "002": 4837660, "003":4837663, "004":4837665, "006":4837668, "008": 4837685, "009": 4837698, "010":4837710, "012": 4837713, "015": 4837714, "alts":4837716},
    "Module 3: HW":   {"001": 4884452, "002": 4884574, "003":4884573, "004":4884572, "006":4884571, "008": 4884569, "009": 4884568, "010":4884567, "012": 4884566, "015": 4884554},
    "Module 4: Exam": {"all":4945161, "alt": 4971542},
    "Module 5: Quiz": {"001": 4987891, "002": 4987992, "003":4987996, "004":4988010, "006":4988012, "008": 4988019, "009": 4988020, "010":4988022, "012": 4988023, "015": 4988024, "alts":4988036},
    "Module 6: Quiz": {},
    "Module 7: HW": {},
    "Module 8: Exam": {},
    "Module 9: Quiz": {},
    "Module 10: Quiz": {},
    "Module 11: HW": {},
    "Module 12: Exam": {},
    "Module 13: Quiz": {},
    "Module 14: HW": {},
    "Module 15: Quiz": {},
}

################# THE GRADESCOPE API ##############
## 1) add you grade scope credentials to config.yaml
## I have created an account math160gradescopehelper where to the config file is on the shared one drive

## grade scope has updated how they export data but the API has not changed
## The following will fix things
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
    NotYet = "Not Yet"

default_rubric_eval = RubricScore.NotYet.value

# This was only for Mod 1 Spring 2024. SO it should be deleted at some point
class RubricScoreMod1(Enum):
    Satisfactory = "Satisfactory (S)"
    RevisionNeeded = "Minor Revision Needed (MR)"
    NotYet = "Not Yet (NY)"
    NotGradable = "Not Gradable (NG)"
# Also old
class RubricScore_old(Enum):
    Satisfactory = "Satisfactory"
    RevisionNeeded = "Minor Revision"
    NotYet = "Not Yet"
    NotGradable = "Not gradable"

# Change depending on how the gradescope rubric is set up
# currently this is looking for a rubric group called "L2 Rubric Score"
# with the options according to RubricScore
def get_standard_rubric_key(standard="", grade=None):
    return f"{standard} Rubric Score: {"" if grade is None else grade}"




###################### RUNNING THIS SCRIPT #################
# Assignment Name to get evals for. This should match the name in
# BIG_LOOK_UP_TABLE made at the top
ASSIGNMENT_NAME = "Module 4: Exam"
# leave empty to do all sections, or ["001"] do only do section 001
#SECTIONS = list(BIG_LOOK_UP_TABLE[ASSIGNMENT_NAME].keys())
#SECTIONS.pop(SECTIONS.index("010"))
#SECTIONS.pop(SECTIONS.index("009"))
#SECTIONS.pop(SECTIONS.index("004"))
#SECTIONS.pop(SECTIONS.index("012"))
SECTIONS = []#["001", "002", "003", "015"]    # all but  4, 12

ONE_FILE_EACH = False
DRAFT_EMAILS = False

# Run the file ExportFromGradescope.py! or run this file. either will work
# good luck!
if __name__ == '__main__': 
    exec(open("ExportFromGradescope.py").read())

# You can upload the output of the file to canvas via tamper monkey
# check out the following:
# https://oit.colorado.edu/services/teaching-learning-applications/canvas/enhancements-integrations/enhancements

