class packet:
    def __init__(self):
        self.k = 2048
        self.eEelc = 50 * (10**-9)
        self.eAmp = 100 * (10 ** -12)
        self.data = ""

    def __init__(self,data=""):
        self.k = 2048
        self.eEelc = 50 * (10 ** -9)
        self.eAmp = 100 * (10 ** -12)
        self.data = data
    def __str__(self):
        return f'{self.k}\t{self.eEelc}\t{self.eAmp}\t{self.data}'