class MTF:
    def __init__(self):
        self.sym_table = [chr(i) for i in range(256)]

    def transform(self, s: list) -> list:
        transformed = []
        for i in range(len(s)):
            s_idx = self.sym_table.index(chr(s[i]))
            transformed.append(s_idx)
            self.sym_table.insert(0, self.sym_table[s_idx])
            del self.sym_table[s_idx + 1]  # + 1 here to compensate insert above
        return transformed

    def undo_transform(self, transformed: list) -> list:
        origin = []
        for i in range(len(transformed)):
            origin.append(self.sym_table[transformed[i]])
            self.sym_table.insert(0, self.sym_table[transformed[i]])
            del self.sym_table[transformed[i] + 1]  # + 1 to compensate insert
        return origin
