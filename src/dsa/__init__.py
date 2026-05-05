from .data_structures import *
from .algorithms import *
from . import data_structures as ds
from . import algorithms as a

__all__: list[str] = [*ds.__all__, *a.__all__]
