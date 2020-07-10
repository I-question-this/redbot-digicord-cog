#!/usr/bin/env python3
"""Database Class"""
import random
random.seed()

from .digimon import Digimon, Stage

class Database:
    def __init__(self, file_path:str):
        self.diginfo = {}
        # Read in database
        self.diginfo[1] = Digimon("Kuramon", 1, Stage.BABY)

    
    def random_digimon(self) -> Digimon:
        """Returns a random Digimon with a random level
        Returns
        -------
        Digimon:
            A random Digimon with a random level
        """
        # Get a random id number for a Digimon
        random_id = random.randrange(min(self.diginfo), max(self.diginfo)+1)
        # Get Digimon
        d = self.diginfo[random_id]
        # Set to a random level
        d.level = random.randrange(1,101)
        return d

