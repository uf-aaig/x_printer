import pytest
import x_printer.io_templates as io
import x_printer.spaces as spaces

def test_txt_input():
    text_input_path  = "./tests/inputs/input.txt"
    text_wrapper = io.Txt_Wrapper(text_input_path)

    variable_definition_path  = "./tests/inputs/vdef.csv"
    output_path  = "./tests/outputs/output_txt_test.txt"
    var_space = spaces.Variable_Space(variable_definition_path)
    vars = var_space.sample(num=1)
    _ = text_wrapper.instanciate(vars, output_path)
    print("")

test_txt_input()


