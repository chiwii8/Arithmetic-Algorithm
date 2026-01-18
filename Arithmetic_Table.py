from collections import OrderedDict

class FrequencyTable:
    def __init__(self):
        self.alphabet = []
        self.frequencies = OrderedDict()
        self.nsymbols = 0

    def add(self, symbol):
        self.nsymbols += 1
        if symbol in self.frequencies:
            self.frequencies[symbol] += 1
        else:
            self.alphabet.append(symbol)
            self.frequencies[symbol] = 1

    def calculateProbabilities(self):
        probabilities = {}
        for symbol in self.alphabet:
            probabilities[symbol] = self.frequencies[symbol] / self.nsymbols

        ranges = {}
        accumulate = 0.0
        for symbol in self.alphabet:
            ranges[symbol] = (accumulate, accumulate + probabilities[symbol])
            accumulate += probabilities[symbol]

        return probabilities, ranges

    def show_table(self):
        print(f"\n{'=' * 80}")
        print(f"{'Symbol':<10} | {'Frequency':<10} | {'Probability':<12} | {'Low':<12} | {'High':<12}")
        print(f"{'=' * 80}")

        probabilities, accumulate_range = self.calculateProbabilities()

        for symbol in sorted(self.alphabet):
            f = self.frequencies[symbol]
            p = probabilities[symbol]
            low, high = accumulate_range[symbol]
            print(f"{str(symbol):<10} | {f:<10} | {p:<12.6f} | {low:<12.6f} | {high:<12.6f}")

        print(f"{'=' * 80}\n")
