import random

class OrganismNameGenerator:
    def __init__(self):
        # Expanded list of Latin words for generating names
        self.latin_words = [
            "viridis", "caeruleum", "albus", "alter", "flavus", "ruber",
            "aureus", "glacialis", "aridus", "silvaticus", "marinus",
            "montanus", "aquaticus", "nocturnus", "solaris", "ventosus",
            "humilis", "fortis", "celeris", "candidus", "clarus", "tenebris",
            "serenus", "cruentus", "gracilis", "magnus", "parvus", "longus",
            "brevis", "altus", "planus", "durus", "mollis", "dulcis", "asper",
            "vividus", "saevus", "ferox", "levis", "tardus", "rapidus",
            "fidelis", "ignotus", "notus", "callidus", "ignis", "aqua",
            "terra", "aer", "lux", "umbra", "nox", "dies", "sideralis",
            "stellatus", "lunaris", "fulgur", "nebula", "pluvialis",
            "gelidus", "calidus", "frigida", "aestivus", "hibernus", "vernal",
            "autumnus", "aurora", "densus", "liquidus", "solidus", "saxum",
            "herba", "flos", "fructus", "radix", "folium", "spina", "ramus",
            "cervus", "ursus", "lepus", "avis", "aquila", "serpens", "pisces",
            "lupus", "vulpes", "felis", "leo", "corvus", "equus", "bubo",
            "musca", "lacerta", "pavo", "testudo", "delphinus", "scorpius",
            "ignavus", "pugnax", "solitarius"
        ]

    def _generate_random_name(self, base):
        """Helper method to generate a name using a base type and a random Latin word."""
        latin_word = random.choice(self.latin_words)
        return f"{base} {latin_word}"

    def generate_passive_name(self):
        """Generate a name for a passive organism."""
        return self._generate_random_name("passive")

    def generate_herbivore_name(self):
        """Generate a name for a herbivore organism."""
        return self._generate_random_name("herbivore")

    def generate_carnivore_name(self):
        """Generate a name for a carnivore organism."""
        return self._generate_random_name("carnivore")
