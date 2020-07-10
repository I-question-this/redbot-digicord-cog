#!/usr/bin/env python3
"""Digimon Class"""

from enum import Enum

class Stage(Enum):
    BABY="Baby"
    IN_TRAINING="In-Training"
    ROOKIE="Rookie"
    CHAMPION="Champion"
    ULTIMATE="Ultimate"
    MEGA="Mega"
    ULTRA="Ultra"
    ARMOR="Armor"
    NONE="None"

    @classmethod
    def from_string(cls, string:str):
        """Returns the Enum associated with a given string.
        Parameters
        ----------
        string: str
            A string containing the name of the Enum we want.
            Note that it will be converted to all uppercase,
            and '-' characters will be replaced with '_' 
            characters for convenience.
        Returns
        -------
        Stage:
            The desired Enum value
        """
        # Simplifies string to enum conversion
        return cls[string.upper().replace("-","_")]



class Species:
    def __init__(self, name:str, number:int, stage:Stage):
        self.name = name
        self.number = number
        self._stage_enum = stage


    def to_dict(self) -> dict:
        """Returns all parameters needed to recreate this object

        Returns
        -------
        dict:
            Parameters needed to recreate this object
        """
        parameters = {}
        parameters["name"] = self.name
        parameters["number"] = self.number
        parameters["stage"] = self.stage
        return parameters


    @staticmethod
    def from_dict(parameters:dict):
        """Creates an instance of this object with the given dictionary"""
        if isinstance(parameters["stage"], str):
            parameters["stage"] = Stage.from_string(parameters["stage"])

        return Species(
            name=parameters["name"],
            number=parameters["number"],
            stage=parameters["stage"]
        )


    @property
    def stage(self) -> str:
        """Gets the stage name.
        The stage is saved as an enum, but this returns just
            the name.
        Returns
        -------
        str
            The name of the stage this Digimon is in.
        """
        return self._stage_enum.value


class Individual:
    def __init__(self, number:int, nickname:str=None, level:int=None):
        self.number = number
        self.nickname = nickname
        if level is None or level < 1:
            self.level = 1
        elif level > 100:
            self.level = 100
        else:
            self.level = level


    def to_dict(self) -> dict:
        """Returns all parameters needed to recreate this object

        Returns
        -------
        dict:
            Parameters needed to recreate this object
        """
        parameters = {}
        parameters["nickname"] = self.nickname
        parameters["number"] = self.number
        parameters["level"] = self.level
        return parameters


    @staticmethod
    def from_dict(parameters:dict):
        """Creates an instance of this object with the given dictionary"""
        return Individual(
            nickname=parameters["nickname"],
            number=parameters["number"],
            level=parameters["level"]
        )

