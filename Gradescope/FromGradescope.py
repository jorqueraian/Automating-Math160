# Im going to try this: https://pypi.org/project/gradescope/
# but really im using this https://github.com/mooey5775/gradescope/tree/master which used the above

import gradescope
from enum import Enum
import re
import pandas as pd
import csv

BIG_LOOK_UP_TABLE = {
    "Module 1: Quiz": 3952727,
}
BIG_LOOK_UP_TABLE_versioned = {
    "Module 1: Quiz": [3952727],
    "Module 2: Quiz": [3989512, 4004592]
}


## ugghhh their code is broke. but i fixed it
gradescope.util.NUM_HOUSEKEEPING_COLS = 13

GRADESCOPE_COURSE_NUMBER = 703259

def get_standard_rubric_key(standard, grade): # possible point of failure. need the rubrics to be labeled in a very specific way!
    return f"**{standard}**: Rubric Score: {grade}"

class RubricScore(Enum):
    Satisfactory = "Satisfactory (S)"
    RevisionNeeded = "Minor Revision Needed (MR)"
    NotYet = "Not Yet (NY)"
    NotGradable = "Not Gradable (NG)"


def add_rubric_scores(grades_and_evals):
    for student in grades_and_evals:
        student["rubric score"] = {}  # add new dictionary key for scores
        for key in list(student["questions"].keys()):
            if re.match(r"\d{1,2}: \w\d{1,2} .*", key):
                standard = key.split(" ")[1]  # possible point of failure. need the questions to be labeled in a very specific way!
                score = RubricScore.NotGradable.value
                for rub_score in RubricScore:
                    if student["questions"][key]["rubric_items"][get_standard_rubric_key(standard, rub_score.value)]:
                        score = rub_score.value
                student["rubric score"][standard] = score.split(" (")[0]


def save_assignment_to_csv(assignment_name, canvas_df):
    canvas_df.to_csv(f"{assignment_name.replace(':', '').replace(' ', '-')}-results.csv", index=False)


def get_gradescope_data_for_versd_assignment(course_num, assignment_nums, canvas_usable=True, canvas_roster=None):
    evals = []
    for assignment_num in assignment_nums:
        evals_ver = gradescope.get_assignment_evaluations(course_num, assignment_num)
        evals += [eval for eval in evals_ver if eval["Status"] != "Missing"]
    add_rubric_scores(evals)

    if canvas_usable and canvas_roster is not None:
        canvas_df = pd.read_csv(open(canvas_roster, 'rb'), usecols=["Full name", "SIS Id"])
        canvas_id_dict = {row["SIS Id"]: row["Full name"] for _, row in canvas_df.iterrows()}
        assignment_stds = list(evals[0]["rubric score"].keys())
        columns = ["Student Name", "Student ID", "Posted Score", "Attempt Number"] + [f"Rating: {standard}" for standard in assignment_stds]

        rubric_scores = []
        for student in evals:  # skip test student
            if student["SID"] == "123456789":
                continue
            else:
                rubric_scores.append([canvas_id_dict[int(student["SID"])], student["SID"], 1, "null"] + 
                                        [student["rubric score"][std] for std in assignment_stds])
        
        the_frame = pd.DataFrame(rubric_scores, columns=columns)
        return the_frame
    else:
        return evals


def get_gradescope_data_for_assignment(course_num, assignment_num, canvas_usable=True, canvas_roster=None):
    evals = gradescope.get_assignment_evaluations(course_num, assignment_num)
    evals = [eval for eval in evals if eval["Status"] != "Missing"]
    add_rubric_scores(evals)
    if canvas_usable and canvas_roster is not None:
        canvas_df = pd.read_csv(open(canvas_roster, 'rb'), usecols=["Full name", "SIS Id"])
        canvas_id_dict = {row["SIS Id"]: row["Full name"] for _, row in canvas_df.iterrows()}
        assignment_stds = list(evals[0]["rubric score"].keys())
        columns = ["Student Name", "Student ID", "Posted Score", "Attempt Number"] + [f"Rating: {standard}" for standard in assignment_stds]

        rubric_scores = []
        for student in evals:  # skip test student
            if student["SID"] == "123456789":
                continue
            else:
                rubric_scores.append([canvas_id_dict[int(student["SID"])], student["SID"], 1, "null"] + 
                                        [student["rubric score"][std] for std in assignment_stds])
        
        the_frame = pd.DataFrame(rubric_scores, columns=columns)
        return the_frame
    else:
        return evals


# Assignment Name to get evals for
ASSIGNMENT_NAME = "Module 1: Quiz"


evals = get_gradescope_data_for_versd_assignment(GRADESCOPE_COURSE_NUMBER, 
                                                BIG_LOOK_UP_TABLE_versioned[ASSIGNMENT_NAME], 
                                                True, "canvas_students.csv")
save_assignment_to_csv(ASSIGNMENT_NAME, evals)

# this can be uploaded to canvas via tamper monkey
# https://oit.colorado.edu/services/teaching-learning-applications/canvas/enhancements-integrations/enhancements
