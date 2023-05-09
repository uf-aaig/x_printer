# x_printer

Software to simplify the creation of many input files from a defined parameter space:
```
- Read parameterized input file
- Define parameter space 
- Sample from parameter space 
- Populate input file with sampled points 
```

## Folders
```
- x_printer: Main source code 
- tests    : unit tests and example inputs and outputs 
```

## Tests
Run pytest with:
```bash
$ python -m pytest
```

## Test your own inputs
```
- input.txt: Parameterized text file with N variables 
- vdef.csv : Variable definition of the N variables in the"input.txt" file 
```
### input.txt
```
- Input file where the parameter values are replaced with parameterized variable names like "VAR1" or "LENGTH"  
- Any string value may be defined, and will be replaced with a parameter value defined in the "vdef.csv" file 
```
### vdef.csv
```
- Each row corresponds to a variable in the "input.txt" file
- Mulitple rows can correspond to the same variable, defined under different conditions (E.G. VAR1 > 0.1 if VAR2 = "Great Example") 
- Each column defines the possible parameter values as in the following table. There are limited options in initial versions: 
```

| Header Name | Options | Description|
|----------------------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| var             | any string | (E.G. Var1, Var2, EXAMPLE_NAME, ...) |
| var_format      | VALUES, RANGE | Defines how the variable will be defined and read from "var_def" column |
| var_type        | int, float, string | variable type, conditions how variable is read in and output. |
| var_def         | (VALUES: M1;M2;M3;...), (Range: start_num;increment;end_num;...)|Must be semicollon seperated. Variable interpretation depends on the "var_type" declaration|
| precision       | int (>=0)   | The number of decimal places to use in input file instance. Not garunteed unless "force_precision" is "TRUE"|
| force_odd       | TRUE, FALSE | Force the variable to be odd. Must be "FALSE" when var_type is "string," or if "force_even" is TRUE|
| force_even      | TRUE, FALSE | Force the variable to be even. Must be "FALSE" when var_type is "string," or if "force_odd" is TRUE |
| force_precision | TRUE, FALSE | Force the output variable to subscribe to the "precision" value (avoid computational errors). |
| conditional_var | string in "var" list | E.G. Var2 (means) |
| condition_type  | =                    | Only "="" enabeled at this time. Other conditions being considered. |
| condition_def   | The parameter instance | "var" variable will only take on the "var_def" value if "conditional_var" is this value (E.G. "M1"). The full parameter range of "var_def" must be considered, likley by putting multiple rows in the file covering the full parameter range.  |

