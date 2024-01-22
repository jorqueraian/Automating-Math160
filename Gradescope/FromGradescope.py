# Im going to try this: https://pypi.org/project/gradescope/
# but really im using this https://github.com/mooey5775/gradescope/tree/master which used the above

import gradescope
from enum import Enum

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
            standard = key.split(" ")[1]  # possible point of failure. need the questions to be labeled in a very specific way!
            score = RubricScore.NotGradable.value
            for rub_score in RubricScore:
                if student["questions"][key]["rubric_items"][get_standard_rubric_key(standard, rub_score.value)]:
                    score = rub_score.value
            student["rubric score"][standard] = score


def get_gradescope_data_for_assignment(course_num, assignment_num):
    evals = gradescope.get_assignment_evaluations(course_num, assignment_num)
    evals = [eval for eval in evals if eval["Status"] != "Missing"]
    add_rubric_scores(evals)
    return evals


get_gradescope_data_for_assignment(GRADESCOPE_COURSE_NUMBER, 3952727)