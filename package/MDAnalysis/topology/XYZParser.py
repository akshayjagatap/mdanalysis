# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8
#
# MDAnalysis --- http://www.MDAnalysis.org
# Copyright (c) 2006-2015 Naveen Michaud-Agrawal, Elizabeth J. Denning, Oliver Beckstein
# and contributors (see AUTHORS for the full list)
#
# Released under the GNU Public Licence, v2 or any higher version
#
# Please cite your use of MDAnalysis in published work:
# N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein.
# MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.
# J. Comput. Chem. 32 (2011), 2319--2327, doi:10.1002/jcc.21787
#

"""
XYZ Topology Parser
===================

.. versionadded:: 0.9.1

Reads an xyz file and pulls the atom information from it.  Because
xyz only has atom name information, all information about residues
and segments won't be populated.

Classes
-------

.. autoclass:: XYZParser
   :members:
   :inherited-members:

"""
from __future__ import absolute_import

import numpy as np

from ..lib.util import openany
from .base import TopologyReader
from ..core.topology import Topology
from ..core.topologyattrs import (
    Atomnames,
)


class XYZParser(TopologyReader):
    """Parse a list of atoms from an XYZ file.

    .. versionadded:: 0.9.1
    """

    def parse(self):
        """Read the file and return the structure.

        Returns
        -------
        MDAnalysis Topology object
        """
        with openany(self.filename, 'r') as inf:
            natoms = int(inf.readline().strip())
            inf.readline()

            names = np.zeros(natoms, dtype=object)

            # Can't infinitely read as XYZ files can be multiframe
            for i in range(natoms):
                name = inf.readline().split()[0]
                names[i] = name

        names = Atomnames(names)
        top = Topology(natoms, 0, 0,
                       attrs=[names])

        return top