#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from ..constructor import Constructor


def include_shell():
    from .include import Include
    return Include


CONSTRUCTORS = (
    ('Include', Constructor(include_shell)),
)

