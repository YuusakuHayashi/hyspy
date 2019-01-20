class HYFolderer:
    def createDummyFile(self, q):
        i = 0
        while i < q:
            i += 1
            s = str(i)
            fn = 'dummy{0}'.format(s)
            with open(fn, "w"):
                pass
