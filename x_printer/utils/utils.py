import os
import json
import copy


# TODO: Move this all to the x_printer submodule
##########################################################################
# Helper function to enable dot-indexing for dicts
class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError from e

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# Class with common variable definition (of a dimension or a set)
class Var(dotdict):
    def __init__(
        self,
        _name=None,
        _type=None,
        _format=None,
        _values=None,
        _default=None,
        _instance=None,
        _precision=None,
        _conditional_var=None,
        _condition_type=None,
        _condition_def=None,
        **kwargs
    ):
        self.name = _name
        self.type = _type
        self.format = _format
        self.vals = _values
        self.precision = _precision
        self.default = _default
        self.instance = _default
        self.conditional_var = _conditional_var
        self.condition_type = _condition_type
        self.condition_def = _condition_def

    def set(self, value):
        # TODO: Add checks for valid parameter entry
        self.instance = value
        return None


# Container class for all variables (with dot-indexible attributes according to variable name)
class Vars(dotdict):
    def __init__(self, vars):
        super().__init__()
        for var in vars:
            self[var.name] = var
        self.kwargs = {}
        return None

    def add(self, var):
        self[var.name] = var
        return None


# Container for variations of experiments
class Experiments:
    def __init__(self, template_vars, add_default=False):
        super().__init__()
        self.template_vars = copy.deepcopy(template_vars)
        self.experiments = []
        if add_default:
            self.experiments.append(template_vars)

    def __iter__(self):
        return iter(self.experiments)

    def add_var_slice(self, var_name, vals=[], vars=None):
        if vars == None:
            vars = copy.deepcopy(self.template_vars)

        for val in vals:
            experiment = vars
            experiment[var_name].instance = val
            self.experiments.append(experiment)
