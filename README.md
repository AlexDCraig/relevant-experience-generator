Parse LaTeX file, replace dummy values with correct ones: python parser.py

Compile a LaTex file from .tex format, generate pdf: ./run_latex.ps1
Assumes file is named 'main.tex'.

'template.tex' is provided. This is a bare bones look at the illegal values of a resume. Illegal values here are simply values that are phony that we wish to replace with valid ones. In order to execute this suite properly, you need a file called 'proper_values.json' located within this same directory that maps the illegal values to the valid ones.
