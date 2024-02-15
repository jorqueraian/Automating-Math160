# EVERYTHING HERE CAN BE CHANGED, JUST READ THE DESCRIPTION BEFORE DOING SO
# GO TO THE BOTTOM WHEN RUNNING THIS SCRIPT

############# GRADESCOPE COURSE NUMBER #############
# This comes from the url https://www.gradescope.com/courses/703259
GRADESCOPE_COURSE_NUMBER = 703259

############ CANVAS ROSTER #####################
# export directly from canvas and save the csv in this file system
# you may need to add Gradescope/ in font of the name if you put it in the gradescope folder
CANVAS_ROSTER = "canvas_students.csv"

############## PUT ASSIGNMENT NUMBERS HERE AS FOLLOWS #############
####    "Name of assignment" : [assignment ids for each version]
### assignment ids also come from url https://www.gradescope.com/courses/703259/assignments/3989512
BIG_LOOK_UP_TABLE = {
    "Module 1: Quiz": {"all": 3952727},
    "Module 1: Quiz alts": {"alts": 4031687},
    "Module 2: Quiz": {"idk": 4009270},  # Already published: 3989512, 4009272  # Joel: not used 4009266 
    "Module 2: Quiz alts": {"alts": 4031746},
    "Module 3: Quiz": {"001":4025219, "003":4025034, "004": 4025220, "005":4025222, "008":4025234, "009":4025236, "006":4025276},
    "Module 4: Exam": {"all": 4065801, "sdc": 4082832, "alts": 4075164}

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
ASSIGNMENT_NAME = "Module 4: Exam"
# leave empty to do all sections, or ["001"] do only do section 001
SECTIONS = []

# Run the file ExportFromGradescope.py! or run this file. either will work
# good luck!
if __name__ == '__main__': 
    exec(open("Gradescope/ExportFromGradescope.py").read())

# You can upload the output of the file to canvas via tamper monkey
# check out the following:
# https://oit.colorado.edu/services/teaching-learning-applications/canvas/enhancements-integrations/enhancements

