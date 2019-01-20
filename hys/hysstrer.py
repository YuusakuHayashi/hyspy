class HysStrer:
    def __init__(self, string):
        self.string = string    

    def padZenSpace(self, char_cnt, direction="right"):
        return self.string + "　" * (char_cnt - len(self.string))
