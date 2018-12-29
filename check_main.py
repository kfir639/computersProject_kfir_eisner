from main import fit_linear

input_files = [".//inputOutputExamples//workingRows//input.txt",
               ".//inputOutputExamples//workingCols//input.txt",
               ".//inputOutputExamples//errSigma//input.txt",
               ".//inputOutputExamples//errDataLength//input.txt",
               ".//inputOutputExamples//errDataLength//input2.txt",
               ]


for i, input_file in enumerate(input_files):
    fit_linear(input_file, fit_interval=i)