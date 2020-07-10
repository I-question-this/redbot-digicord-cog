#!/usr/bin/env python3
"""Database Class"""
import random
random.seed()

from .digimon import Individual, Species, Stage

class Database:
    def __init__(self, file_path:str):
        self.diginfo = {}
        # Read in database
        self.diginfo[1] = Species("Kuramon", 1, Stage.BABY)

    
    def random_digimon(self) -> Individual:
        """Returns a random Digimon with a random level
        Returns
        -------
        Individual:
            A random Digimon with a random level
        """
        # Get a random id number for a Digimon
        random_species_number = random.randrange(
                min(self.diginfo), max(self.diginfo)+1)
        # Create an Individual
        i = Individual(random_species_number)
        # Set to a random level
        i.level = random.randrange(1,101)
        return i

