from collections import OrderedDict
""" Implementation of the Arithmetic code without normalization
    This is doing for chains of text using float, only use with short words"""
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
class ArithCodding:
    def __init__(self):
        self.precision = 32
        self.max_val = (1 << self.precision) - 1

    def buildFrequencyTable(self, message):
        frequencyTable = FrequencyTable()
        for char in message:
            frequencyTable.add(char)

        return frequencyTable

    def encode(self, message: str):
        table = self.buildFrequencyTable(message)
        probabilities, ranges = table.calculateProbabilities()
        low = 0.0
        high = 1.0

        for symbol in message:  # iterar directamente sobre la cadena
            r_low, r_high = ranges[symbol]
            range_width = high - low
            high = low + range_width * r_high
            low = low + range_width * r_low

        code = (low + high) / 2
        return code, probabilities

    def decode(self, code, prob, longitude):
        ranges = {}
        init = 0.0
        alphabet = prob.keys()

        for symbol, p in prob.items():
            ranges[symbol] = (init, init + prob[symbol])
            init += prob[symbol]

        text = ""

        for _ in range(longitude):
            for symbol, (r_low, r_high) in ranges.items():
                if r_low <= code < r_high:
                    text += symbol
                    code = (code - r_low) / (r_high - r_low)
                    break

        return text


if __name__ == "__main__":
    message2 = "Texto Corto"
    message = "ABACA"
    arith = ArithCodding()

    codigo, probs = arith.encode(message)
    print("Código comprimido:", codigo)

    decoded = arith.decode(codigo, probs, len(message))
    print("Texto decodificado:", decoded)

    codigo2, probs2 = arith.encode(message2)
    print("Código comprimido:", codigo2)

    decoded2 = arith.decode(codigo2, probs2, len(message2))
    print("Texto decodificado:", decoded2)
