import json
from pymatgen.analysis.reaction_calculator import Reaction
from pymatgen.core.composition import Composition


__autor__ = 'Jherfson Castro Gomes'
__email__ = 'jherfson.castro@gmail.com'
__version__ = '2020.21.11'
__date__ = 'apr 24, 2020'


class Stoichiometric():
    """[summary]
    """
    def __init__(self, equation, mass_production):
        """[summary]

        Args:
            equation ([type]): [description]
            mass_production ([type]): [description]
        """
        self.equation = equation
        self.mass_production = mass_production

        # fazendo a separação da reagente do produto
        self.separate_rp = self.equation.split('->')

        # separando os reagente para passar para Classe Composition
        self.reagent = self.separate_rp[0].split('+')

        # separando os produtos para passar para Classe Composition
        self.producer = self.separate_rp[1].split('+')

        reactants = [Composition(i) for i in self.reagent]
        producers = [Composition(i) for i in self.producer]


        self.reaction = Reaction(reactants, producers)
        print(self.reaction)

        self.mol_reactant = []
        self.mol_production = []
        self.mass_reactant = []
        self.massa_production = []

        tam = int(len(producers))
        
        j = 0

        for i in range(len(self.reaction.coeffs)):
            if i < tam:
                mol = (self.reaction.coeffs[i]/self.reaction.coeffs[-tam]) * (mass_production/Composition(self.producer[-tam]).weight)
                self.mol_reactant.append(mol)
                mass = mol * Composition(self.reagent[i]).weight
                self.mass_reactant.append(mass)
            else:
                mol_ = (self.reaction.coeffs[i]/self.reaction.coeffs[-tam]) * (mass_production/Composition(self.producer[-tam]).weight)
                self.mol_production.append(mol_)
                mass_ = mol_ * Composition(self.producer[j]).weight
                j = j + 1
                self.massa_production.append(mass_)


    def to_dict(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        # composto
        comp = self.reagent.copy()
        comp.extend(self.producer)

        # mol
        mol = self.mol_reactant.copy()
        mol.extend(self.mol_production)

        # mass
        massa = self.mass_reactant.copy()
        massa.extend(self.massa_production)

        chemical_compounds = []
        for i in range(len(self.reaction.coeffs)):
            x = {comp[i]: {'coefciente': round(self.reaction.coeffs[i], 4), 'peso molecular': round(Composition(comp[i]).weight, 4), 'mol': round(mol[i], 4), 'massa': round(massa[i], 4)}}
            chemical_compounds.append(x)

        return chemical_compounds


    def to_json(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return json.dumps(self.to_dict(), indent=4, separators=(", ", " : "))


    def print_mass(self):
        """[created a new function that prints the compound and the dough]

        Returns:
            [dict]: [compound and mass in grams. "Li2CO3 " : (-0.4466)g]
        """
        mass = self.to_dict()
        result = {}

        for i in range(len(mass)):
            for composto, massa in mass[i].items():
                result[composto] = massa['massa']
     
        return json.dumps(result, indent=4, separators=(", ", " : "))