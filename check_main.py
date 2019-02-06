from main import fit_linear, search_best_parameter

input_files = [
               ".//inputOutputExamples//workingRows//input.txt",
               ".//inputOutputExamples//workingRows//input2.txt",
               ".//inputOutputExamples//workingCols//input.txt",
               ".//inputOutputExamples//workingCols//input2.txt",
               ".//inputOutputExamples//errSigma//input.txt",
               ".//inputOutputExamples//errDataLength//input.txt",
               ".//inputOutputExamples//errDataLength//input2.txt",
               ]


search_best_parameter(".//inputOutputExamples//bonus//input.txt")

for i, input_file in enumerate(input_files):
    print(input_file)
    fit_linear(input_file, fit_interval=i+1)

