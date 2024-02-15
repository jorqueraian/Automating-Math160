import os
import pandas as pd
import re
import glob
os.chdir(os.path.dirname(__file__))

OUTPUT_DIR = "output/"

# maybe make dict to have number of times needed to get mastery
STANDARDS = ["T1","T2",
             "L1","L2","L3","L4","L5","L6","L7",
             "D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11",
             "I1","I2"]


def read_n_combine(rubrics_dir):
    # If only i knew how to use data frames this would have been a single line! and 100x faster. But what ever
    rubrics = glob.glob(f"{rubrics_dir}/*.csv")
    #combined_df = pd.DataFrame(columns=["Student Name","Student ID"]+STANDARDS)
    combined_dict = {}
    # structure here is {student name + student id: {standard: count}}
    for r in rubrics:
        rubric_df = pd.read_csv(r)
        stds_assessed = rubric_df.columns[4:]
        for _, row in rubric_df.iterrows():
            if row["Student Name"] == "Test Student":
                continue
            posted_score = row["Posted Score"]
            if (row["Student Name"], int(row["Student ID"])) not in combined_dict.keys():  # and combined_df['Student ID'] == row['Student ID']) & (df['B'] == 3)).any():
                combined_dict[(row["Student Name"], int(row["Student ID"]))]= {standard:0 for standard in STANDARDS}
            for standard_key in stds_assessed:
                standard = standard_key.split(": ")[-1]
                # idk do a check with posted score or something
                if posted_score == 1 and row[standard_key] == float("nan"):
                    print(f'Student: {row["Student Name"]} received no rubric score on {standard} in {r}. But their posted score is 1 (Complete)!')
                if row[standard_key] == "Satisfactory":
                    combined_dict[(row["Student Name"], int(row["Student ID"]))][standard] += 1
    rubric_totals = []
    for student, id in list(combined_dict.keys()):  # skip test student
        if id == "123456789":
            continue
        else:
            rubric_totals.append([student, int(id)] + [combined_dict[(student, id)][std] for std in STANDARDS])
        
    the_dframe = pd.DataFrame(rubric_totals, columns=["Student Name", "Student ID"]+STANDARDS)
    return the_dframe


def save_assignment_to_csv(canvas_df):
    from datetime import date
    today = date.today()
    canvas_df.to_csv(f"Grade Report-{today.strftime('%m-%d')}.csv", index=False)



#print("Nothing")
#onlyfiles = [f for f in os.listdir("Rubric Scores") if os.path.isfile("".join(["Rubric Scores", f]))]
combined_scores = read_n_combine("Rubric Scores")
save_assignment_to_csv(combined_scores)
