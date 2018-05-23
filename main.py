import os
import numpy as np
from pdbfixer import PDBFixer
from simtk import openmm, unit
from simtk.openmm import app
import mdtraj
import nglview
from openmmtools.testsystems import TestSystem as _ommtools_TestSystem


_systems_names=[ 'TrpCageImplicit',
                 'BarnaseVacuum',
                 'BarstarVacuum',
                 'BarnaseBarstarVacuum'
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


class BarnaseVacuum(TestSystem):

    def __init__(self,constraints=app.HBonds, hydrogenMass=None, pH=7.0, **kwargs):

        TestSystem.__init__(self, **kwargs)

        system_pdb=PDBFixer(os.path.dirname(__file__)+"/pdbs/Barnase.pdb")

        forcefield = app.ForceField('amber14-all.xml')
        modeller = app.Modeller(system_pdb.topology, system_pdb.positions)
        addHs_log = modeller.addHydrogens(forcefield, pH=pH)

        self.topology  = modeller.getTopology()
        self.positions = modeller.getPositions() # asNumpy=True
        self.system    = forcefield.createSystem(modeller.topology,implicitSolvent=None,
                                         constraints=constraints,nonbondedMethod=app.NoCutoff,
                                         hydrogenMass=hydrogenMass)

class BarstarVacuum(TestSystem):

    def __init__(self,constraints=app.HBonds, hydrogenMass=None, pH=7.0, **kwargs):

        TestSystem.__init__(self, **kwargs)

        system_pdb=PDBFixer(os.path.dirname(__file__)+"/pdbs/Barstar.pdb")

        forcefield = app.ForceField('amber14-all.xml')
        modeller = app.Modeller(system_pdb.topology, system_pdb.positions)
        addHs_log = modeller.addHydrogens(forcefield, pH=pH)

        self.topology  = modeller.getTopology()
        self.positions = modeller.getPositions() # asNumpy=True
        self.system    = forcefield.createSystem(modeller.topology,implicitSolvent=None,
                                         constraints=constraints,nonbondedMethod=app.NoCutoff,
                                         hydrogenMass=hydrogenMass)

class BarstarVacuum(TestSystem):

    def __init__(self,constraints=app.HBonds, hydrogenMass=None, pH=7.0, **kwargs):

        TestSystem.__init__(self, **kwargs)

        system_pdb=PDBFixer(os.path.dirname(__file__)+"/pdbs/Barstar.pdb")

        forcefield = app.ForceField('amber14-all.xml')
        modeller = app.Modeller(system_pdb.topology, system_pdb.positions)
        addHs_log = modeller.addHydrogens(forcefield, pH=pH)

        self.topology  = modeller.getTopology()
        self.positions = modeller.getPositions() # asNumpy=True
        self.system    = forcefield.createSystem(modeller.topology,implicitSolvent=None,
                                         constraints=constraints,nonbondedMethod=app.NoCutoff,
                                         hydrogenMass=hydrogenMass)

class BarnaseBarstarVacuum(TestSystem):

    def __init__(self,constraints=app.HBonds, hydrogenMass=None, pH=7.0, **kwargs):

        TestSystem.__init__(self, **kwargs)

        system_receptor_pdb=PDBFixer(os.path.dirname(__file__)+"/pdbs/Barnase.pdb")
        system_ligand_pdb  =PDBFixer(os.path.dirname(__file__)+"/pdbs/Barstar.pdb")

        forcefield = app.ForceField('amber14-all.xml')
        modeller_receptor = app.Modeller(system_receptor_pdb.topology, system_receptor_pdb.positions)
        addHs_receptor_log = modeller_receptor.addHydrogens(forcefield, pH=pH)
        modeller_ligand = app.Modeller(system_ligand_pdb.topology, system_ligand_pdb.positions)
        addHs_ligand_log = modeller_ligand.addHydrogens(forcefield, pH=pH)

        modeller_complex = app.Modeller(modeller_receptor.getTopology(),modeller_receptor.getPositions())
        modeller_complex.add(modeller_ligand.getTopology(),modeller_ligand.getPositions())

        self.topology  = modeller_complex.getTopology()
        self.positions = modeller_complex.getPositions() # asNumpy=True
        self.system    = forcefield.createSystem(modeller_complex.topology,implicitSolvent=None,
                                         constraints=constraints,nonbondedMethod=app.NoCutoff,
                                         hydrogenMass=hydrogenMass)
