import random
from itertools import product
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


class ECA:
    triple_bits = [list(tup) for tup in list(product([1, 0], repeat=3))]

    def __init__(self, configuration):
        self.configuration = configuration
        self.history = []
        self.rule = None

    @staticmethod
    def bin_from_int(x):
        wolfram_code = [int(bit) for bit in format(x, f'08b')]
        return wolfram_code

    @staticmethod
    def get_neighborhoods(lst):
        n = len(lst)
        neighborhoods = [[lst[(i - 1) % n], lst[i], lst[(i + 1) % n]] for i in range(n)]
        return neighborhoods

    @staticmethod
    def eca_step(rule_number, configuration):
        rule = ECA.bin_from_int(rule_number)
        neighborhoods = ECA.get_neighborhoods(configuration)
        next_configuration = [rule[ECA.triple_bits.index(neighborhood)] for neighborhood in neighborhoods]
        return next_configuration

    @classmethod
    def init_random(cls, configuration_size):
        if not isinstance(configuration_size, int) or configuration_size < 1:
            raise ValueError("Configuration_size must be a positive integer (1 or greater)")
        return cls([random.randint(0, 1) for _ in range(configuration_size)])

    @classmethod
    def init_config(cls, configuration):
        if not isinstance(configuration, list):
            raise TypeError("Configuration must be a list")
        if not all([bit == 0 or bit == 1 for bit in configuration]):
            raise ValueError("Configuration must be a list of 0 and 1")
        return cls(configuration)

    def evolve(self, rule_number, steps):
        if not 0 <= rule_number <= 255:
            raise ValueError("Rule_number must be a number between 0 and 255")
        self.rule = rule_number
        result = [self.configuration, self.eca_step(rule_number, self.configuration)]
        for _ in range(steps - 1):
            result.append(self.eca_step(rule_number, result[-1]))
        self.history = result
        return self.history

    def visualize(self):
        plt.imshow(self.history, cmap='binary')
        plt.xlabel('Cell Index')
        plt.ylabel('Time Step')
        plt.title(f'Space-time Diagram of the ECA {self.rule}')
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.show()
