import generators.LFSR

class Geffe:
    __results = []

    def __init__(self, l1, l2, l3):
        self.__X = l1
        self.__Y = l2
        self.__S = l3

    def next(self):
        x = self.__X.next()
        y = self.__Y.next()
        s = self.__S.next()

        res = x if s == 1 else y
        self.__results.append(res)

        return res

    def get_results(self):
        return self.__results
