import os
import numpy as np
from pdbfixer import PDBFixer
from simtk import openmm, unit
from simtk.openmm import app
import mdtraj
import nglview
from openmmtools.testsystems import TestSystem as _ommtools_TestSystem


_systems_names=[ 'TrpCageImplicit',
]

def _make_nglview(topology=None,positions=None):

    mdtraj_aux_topology = mdtraj.Topology.from_openmm(topology)
    traj_aux = mdtraj.Trajectory(positions._value, mdtraj_aux_topology)
    view = nglview.show_mdtraj(traj_aux)
    view.center()
    return view

def get_systems_names():

    return _systems_names

class TestSystem (_ommtools_TestSystem):

    def __init__(self, **kwargs):

        _ommtools_TestSystem.__init__(self, **kwargs)

        return

    def make_nglview(self):

        return _make_nglview(self.topology,self.positions)

class TrpCageImplicit(TestSystem):

    def __init__(self, constraints=app.HBonds, hydrogenMass=None, pH=7.0, **kwargs):

        TestSystem.__init__(self, **kwargs)

        from pkg_resources import resource_filename
        system_pdb=PDBFixer(os.path.dirname(__file__)+"/pdbs/1l2y.pdb")

        system_pdb.findMissingResidues()
        system_pdb.findNonstandardResidues()
        system_pdb.findMissingAtoms()
        system_pdb.addMissingAtoms()

        forcefield = app.ForceField('amber96.xml', 'amber96_obc.xml')
        modeller = app.Modeller(system_pdb.topology, system_pdb.positions)
        addHs_log = modeller.addHydrogens(forcefield, pH=pH)

        self.topology  = modeller.getTopology()
        self.positions = modeller.getPositions() # asNumpy=True
        self.system    = forcefield.createSystem(modeller.topology,implicitSolvent=app.OBC1,
                                         constraints=constraints,nonbondedMethod=app.NoCutoff,
                                         hydrogenMass=hydrogenMass)

