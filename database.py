#!/usr/bin/env python3
"""Database Class"""
import logging
import random
random.seed()

from .digimon import Individual, Species, Stage


log = logging.getLogger("red.digicord")


class Database:
    def __init__(self, file_path:str):
        self._diginfo = {}
        # Read in database
        self._diginfo[1] = Species("Kuramon", 1, Stage.BABY)

    
    def random_digimon(self) -> Individual:
        """Returns a random Digimon with a random level
        Returns
        -------
        Individual:
            A random Digimon with a random level
        """
        # Get a random id number for a Digimon
        random_species_number = random.randrange(
                min(self._diginfo), max(self._diginfo)+1)
        # Create an Individual
        i = Individual(random_species_number)
        # Set to a random level
        i.level = random.randrange(1,101)
        return i


    def species_information(self, id:int) -> Species:
        """Returns Species information for a given species id number
        
        Parameters
        ----------
        id: int
            The species id number to get information for.

        Returns
        -------
        Species:
            The species information
        """
        spec = self._diginfo.get(id, None)
        if spec is None:
            LOG.critical(f"No such species number: {id}")
        return spec

