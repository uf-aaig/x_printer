import pytest
import x_printer.spaces as spaces

def test_variables():
    print("Checking variable creation...")
    variable_definition_path  = "./tests/inputs/vdef.csv"
    _ = spaces.Variable_Space(variable_definition_path)
    print("")

def test_sample():
    variable_definition_path  = "./tests/inputs/vdef.csv"
    vars = spaces.Variable_Space(variable_definition_path)
    var = vars.sample(num=10)
    print(var)
    print("")


