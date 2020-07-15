#!/usr/bin/env python3
"""Database Class"""
import logging
import random
import json
random.seed()

from .digimon import Individual, Species, Stage


LOG = logging.getLogger("red.digicord")


class UnknownSpeciesNumber(Exception):
    def __init__(self, species_number:int):
        self.species_number = species_number

    def __str__(self):
        return f"Unknown species number: {self.species_number}"



class Database:
    def __init__(self, file_path:str):
        self._diginfo = dict()
        # Read in database
        # self._diginfo[1] = Species("Kuramon", 1, Stage.BABY)
        database = json.load(open('util/database.json'))
        for entry in database:
            self._diginfo[entry['species_number']] = Species(
                    entry['name'],
                    entry['species_number'],
                    Stage.from_string(entry['stage'])
            )



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
        # Get species info
        spec = self.species_information(random_species_number)
        # Create an Individual
        i = Individual(random_species_number, spec.name)
        # Set to a random level
        i.level = random.randrange(1,101)
        return i


    def species_information(self, species_number:int) -> Species:
        """Returns Species information for a given species id number
        
        Parameters
        ----------
        species_number: int
            The species id number to get information for.

        Returns
        -------
        Species:
            The species information

        Raises
        ------
        UnknownSpeciesNumber
           Indicates the species_number is beyond our understanding.
           There is no good reason for this to occur as user input
           should never cause this.
        """
        try:
            return self._diginfo[species_number]
        except KeyError:
            LOG.exception(f"No such species number: {id}")
            raise UnknownSpeciesNumber(species_number)

