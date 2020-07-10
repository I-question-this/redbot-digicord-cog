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



class Digimon:
    def __init__(self, name:str, number:int, stage:Stage,
            nickname:str=None, level:int=None):
        self.name = name
        self.number = number
        self._stage_enum = stage
        self._nickname = nickname
        if level is None or level < 1:
            self.level = 1
        elif level > 100:
            self.level = 100
        else:
            self.level = level


    def __repr__(self):
        """Returns the representation of this Digimon.
        The representation is a string, that if executed
            as Python code would recreate this object.
        This requires that the object be set up to have no
            values saved beyond what can be derived from the
            parameters in it's constructor method.
        Returns
        -------
        str:
            A string of Python code that if executed would 
                recreate this object.
        """
        r = f"{self.__class__.__name__}("
        r += f"name='{self.name}',"
        r += f"number={self.number},"
        r += f"stage=Stage.from_string('{self.stage}'),"
        if self._nickname is None:
            r += f"nickname=None,"
        else:
            r += f"nickname='{self._nickname}',"
        r += f"level={self.level}"
        r += ")"
        return r


    @property
    def nickname(self) -> str:
        """Gets the nickname, or just the species name.
        Returns
        -------
        str
            The "nickname" of the Digimon
        """
        if self._nickname is not None:
            return self._nickname
        else:
            return self.name


    @nickname.setter
    def nickname(self, new_nickname:str):
        """Sets nickname for the Digimon
        Parameters
        ----------
        new_nickname: str
            The new nickname
        """
        self._nickname = new_nickname


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


