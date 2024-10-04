class DifferentAlphabetError(Exception):
    def __init__(self, element):
        self.messenge = f'Element {element} not in fit data set. Please, refit model using custom alphabet.'
        super().__init__(self.messenge)