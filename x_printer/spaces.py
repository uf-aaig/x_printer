import pandas as pd 
import numpy as np 
import random

# Class to read variable definition, verify parameter values, and resolve dependencies
class Variable_Space(): 
    def __init__(self, variable_definition_path):

        self.var_def   = pd.read_csv(variable_definition_path) 

        self.names           = self.var_def["var"].to_list()
        self.var_types       = self.var_def["var_type"].to_list()
        self.conditioned_var = self.var_def["conditional_var"].to_list()
        self.condition_type  = self.var_def["condition_type"].to_list()

        self.var_vals  = []
        for i in range(len(self.names)): 

            # Read parameter values 
            if self.var_def["var_format"][i] == "RANGE": 
                precision      = int(self.var_def["precision"][i]); 
                start_inc_stop = self.var_def["var_def"][i].split(";"); 

                start = round(float(start_inc_stop[0]), precision)
                inc   = round(float(start_inc_stop[1]), precision)
                stop  = round(float(start_inc_stop[2]), precision)

                #self.var_def["var_def"][i] = list(np.linspace(start, stop, int((stop-start + inc)/inc)))
                vals = [start + inc*i for i in range(int(np.floor((stop-start)/inc))+1)]
                if vals[len(vals)-1] != stop: 
                    vals.append(stop)
                self.var_def["var_def"][i] = vals

            elif self.var_def["var_format"][i] == "VALUES": 
                valList = self.var_def["var_def"][i].split(";"); 
                self.var_def["var_def"][i] = valList

    # Get parameter names
    def names(self): 
        return self.names

    def check_and_sample(val, start, stop, inc): 
        if val < start or val > stop: 
            val = round(random.sample(np.linspace(start, stop, int((stop-start)/inc)),1)[0],4)
        return val, 1

    def __sample_list(self, sample_list, s_type): 
        if s_type == "random": 
            return random.sample(sample_list, 1)[0] 
        else: 
            print("Sample type '{}' not an option. Returning random sample... ".format(s_type))
            return random.sample(sample_list, 1)[0]

    # Get the minimum value of a given parameter
    def sample(self, num=1, s_type="random"): 
        samples = []

        for i in range(num): 
            got_all_params = False 
            vid = 0
            sample = {}
            while not got_all_params: 
                
                var                 = self.names[vid]
                conditional_var     = self.conditioned_var[vid]
                need_condition      = not isinstance(conditional_var, type(np.nan))
                condition_in_sample = conditional_var in list(sample.keys())

                if var not in list(sample.keys()) and (not need_condition or condition_in_sample): 

                    var_def_subset = self.var_def[self.var_def["var"] == var]

                    if not need_condition: 
                        sample[var] = self.__sample_list(var_def_subset["var_def"].tolist()[0],s_type)
                       
                    else: 
                        condition = var_def_subset["conditional_var"].tolist()[0] # Assumes only one condition
                        cond_type = var_def_subset["condition_type"].tolist()[0]  
                        cond_val  = sample[condition] 
                        
                        if cond_type == "=": 
                            var_def_subset = var_def_subset[var_def_subset["condition_def"] == cond_val]
                        else: 
                            print("'{}' is not a valid option for 'condition_type' Only '=' is valid at this time.".format(cond_type))
                        
                        # There should only be one row in this df
                        [rows, _] = np.shape(var_def_subset) 
                        if rows == 1: 
                            sample[var] = self.__sample_list(var_def_subset["var_def"].tolist()[0],s_type)
                        else: 
                            print("Only one row should satisfy the {} {} {} condition, but {} were found".format(condition, cond_type, cond_val, rows))
                            sample[var] = None 

                    # Need to force precision before even/odd or the precision update can counter the even/odd correction
                    if var_def_subset["force_precision"].tolist()[0]: 
                        sample[var] = self.force_precision(sample[var], var_def_subset["precision"].tolist()[0])

                    if not (var_def_subset["force_odd"].tolist()[0] and var_def_subset["force_even"].tolist()[0]):
                        if var_def_subset["force_odd"].tolist()[0]: 
                            sample[var] = self.force_odd(sample[var])
                        if var_def_subset["force_even"].tolist()[0]: 
                            sample[var] = self.force_even(sample[var])

                    # Need to force precision after even/odd to solve numerical precision problem with eveb/odd update
                    if var_def_subset["force_precision"].tolist()[0]: 
                        sample[var] = self.force_precision(sample[var], var_def_subset["precision"].tolist()[0])


                    else: 
                        print("Invalid variable def: Both force even and force odd set True. Doing nothing.")

                # Check if we have all parameters
                if len(sample) == len(np.unique(self.names)): 
                    got_all_params = True
                
                # Check if we need to restart from the beginning
                vid = vid + 1
                if vid == len(self.names): 
                    vid = 0

            samples.append(sample)
        return pd.DataFrame(samples)

    # Helper formatting functions
    def force_odd(self, num): 
        precision  = str(num)[::-1].find('.')
        last_digit = int(str(num)[-1])
        if last_digit % 2 == 0:
            num += 10**(-precision)
            print(10**(-precision))
        return num

    def force_even(self, num): 
        precision  = str(num)[::-1].find('.')
        last_digit = int(str(num)[-1])
        if last_digit % 2 == 1:
            num -= 10**(-precision)
            print(10**(-precision))
        return num

    def force_precision(self, num, precision): 
        if precision == 0: 
            num = int(num)
        else: 
            num = float(int(num*(10**precision)))/(10**precision)
        return num