import pytest
import x_printer.io_templates as io

def test_capsule():
    text_input_path           = "./tests/inputs/input.txt"
    variable_definition_path  = "./tests/inputs/vdef.csv"
    output_path               = "./tests/outputs/output_"

    num_experiments = 3
    inputs = io.Input_Capsule(num_experiments,  text_input_path, variable_definition_path)
    files  = inputs.input_list
    print(files)

    for i in range(num_experiments):  
        print(str(output_path + str(i) + ".txt"))
        inputs.save(i, str(output_path + str(i) + ".txt"))

    print("")

