class LFSR:
    register = []
    xor_indexes = []

    # movement direction <<
    # d = [0, 0, 0, 0, 0, 1]
    def __init__(self, initial_fill, xor_indexes):
        self.register = initial_fill
        self.xor_indexes = xor_indexes

    def next(self):
        res = self.register[0]
        new_item = 0

        # calc new element
        for index in self.xor_indexes:
            new_item ^= self.register[index]

        self.register = self.register[1:]

        self.register.append(new_item)

        return res

    def __len__(self):
        return len(self.register)

    def __str__(self):
        return '({})'.format(', '.join(map(str, self.register)))