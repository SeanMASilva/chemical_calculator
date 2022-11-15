from __future__ import annotations
from abc import ABC

ELEMENT_NAMES = ["hydrogen", "helium", 
                "lithium", "berryllium", "boron", "carbon", "nitrogen", "oxygen", "fluorine", "neon",
                "sodium", "magnesium","aluminium", "silicon", "phosphorous", "sulfur", "chlorine", "argon",
                "potassium", "calcium", 
                    "scandium", "titanium", "vanadium", "chromium", "manganeses", "iron", "cobalt", "nickel", "copper", "zinc",
                    "gallium", "germanium", "arsenic", "seleniuim", "bromine", "krypton"]
ELEMENT_WEIGHTS = [1.008, 4.0026,
                6.94, 9.0122, 10.81, 12.011, 14.007, 15.999, 18.998, 20.180,
                22.990, 24.305, 26.982, 28.085, 30.974, 32.06, 35.45, 39.948,
                39.098, 40.078,
                    44.956, 47.867, 50.942, 51.996, 54.938, 55.845, 58.933, 58.693, 63.546, 65.38,
                    69.723, 72.630, 74.922, 78.971, 79.904, 83.798
                ]
ELEMENT_SYMBOLS = ["H", "He",
                "Li", "Be", "B", "C", "N", "O", "F", "Ne",
                "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
                "K", "Ca",
                    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
                    "Ga", "Ge", "As", "Se", "Br", "Kr"]

ELEMENTS = [None] * len(ELEMENT_NAMES)
ELEMENT_DICT:dict[Element] = dict()


class Element():
    "Element of the periodic table"

    def __init__(self, number:int, name:str, symbol:str, weight:float) -> Element:
        self.number = number
        self.name = name
        self.symbol = symbol
        self.atom_weight = weight

    def __str__(self) -> str:
        return f"Element: {self.name} ({self.symbol}), Weight: {self.atom_weight}"

    def __hash__(self) -> int:
        return hash(self.symbol)
 
'''
class Hydrogen(Element):
    name = "hydrogen"
    atomNum = 1
    atomWeight = 1.008
    symbol = "H"

class Helium(Element):
    name = "helium"
    atomNum = 2
    atomWeight = 4.0026
    symbol = "He"

class Lithium(Element):
    name = "lithium"
    atomNum = 3
    atomWeight = 6.94
    symbol = "Li"
'''
for i in range(len(ELEMENT_NAMES)):
    ELEMENTS[i] = Element(i+1, ELEMENT_NAMES[i], ELEMENT_SYMBOLS[i], ELEMENT_WEIGHTS[i])
    ELEMENT_DICT[ELEMENT_SYMBOLS[i]] = ELEMENTS[i]