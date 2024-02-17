# Math160-Automation
Making things ffaster!

## Bonus Quizzes How to
1) Inside `Bonus Quizzes/problembank` create a directory for the tex file you wish to use. For example you may create a directory `FA23`.
2) Add a tex file for each standard you wish to have, this directory should also contain all figures needed to compile the latex files. This should partial tex file starting with `\item`. an example is show below:
```latex
\item\label{std:L3} {\em L3: I can algebraically evaluate the limit of a function at a point.}\\
  Let $g(x)= \begin{cases} 3x+2 & x< 2 \\ 2 & x=2 \\ (x-1)^2+A & x > 2 \\ \end{cases} $.\\
\begin{enumerate}
    \item Compute $\displaystyle{\lim_{x\rightarrow 2^{-}}g(x)}$.
    \vskip 2in
    \item Compute $\displaystyle{\lim_{x\rightarrow 2^{+}}g(x)}$.
    \vskip 2in
    \item Find a value for $A$ so that $\displaystyle{\lim_{x\rightarrow 2}g(x)}$ exists.
\end{enumerate}
``` 
3) Modify the `standards.csv` file if needed.
4) Add students taking quiz to `students.csv` such that there is no header row. There is no limit to the size of the rows
5) Open `create_quiz.py` and update all variable in the bottom of the file and then run the file

## Gradescope to Canvas How to
1) There is a lot of points of failure in these scripts. So before running update all necessary files: re-download `canvas_students.csv` from canvas (For the time being this file should be saved in the parent directory), re-sync Canvas roster on Gradescope. Update `config.yaml` (DO NOT COMMIT THIS UPDATED FILE TO GITHIB) and this file should be saved in the `Gradescope` directory.
2) Fill out the `GradescopeConfig.py` file. This should also walk you through all other set up instructions.
3) You can run either the `GradescopeConfig.py` or the `ExportFromGradescope.py` files. The script may give outputs relating to mistake in the rubric scores.
4) output files will be save in the specified output directory, defaults to `Gradescope/output/`

## Makeup Quizzes
1) Update `MAKEUP_QUIZ_EXCEL`, `MAKEUP_QUIZ_EXCEL_SHEET`, and `QUIZZES_LOCATIONS` variable in `save_makeup_quizzes.py` file as needed.
2) Close the Excel file before running and then run
3) Update Excel file indicating which files have been printed


## Progress Report
1) Export rubric scores from canvas using Tamper Monkey for each assignment you wish to be included, and put these in `Progress Report/Rubric Scores` directory.
2) Update the `STANDARDS_dict` variable as needed in the `generate_progress_reports.py` file.
3) run file

