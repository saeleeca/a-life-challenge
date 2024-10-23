# models/__init__.py
from .genome import CreatureType, Genome
from .organism import Organism
from .passive_organism import PassiveOrganism
from .herbivore_organism import HerbivoreOrganism
from .carnivore_organism import CarnivoreOrganism

__all__ = ['CreatureType', 'Genome', 'Organism', 'PassiveOrganism', 'HerbivoreOrganism', 'CarnivoreOrganism']