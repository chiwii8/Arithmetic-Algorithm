""" Implementation of the Arithmetic code without normalization
    This is doing for chains of text using float, only use with short words"""

from src.Arithmetic_Table import FrequencyTable
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
