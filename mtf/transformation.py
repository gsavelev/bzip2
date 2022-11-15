class MTF:
    def transform(self, s: str) -> list:
        s_list = sorted(list({*s}))  # make ordered list of symbols
        transformed = []
        for i in range(len(s)):
            s_idx = s_list.index(s[i])
            transformed.append(s_idx)
            s_list.insert(0, s_list[s_idx])
            del s_list[s_idx + 1]  # + 1 here to compensate insert above
        return transformed, s_list

    def undo(self, transformed: list, table: list) -> str:
        origin_str = ''
        for i in transformed:
            origin_str += table[i]
            table.insert(0, table[i])
            del table[i + 1]  # + 1 here to compensate insert above
        return origin_str


if __name__ == '__main__':
    mtf = MTF()
    before = 'abacaba'
    after, coding_table = mtf.transform(before)
    after = mtf.undo(after, coding_table)
    assert before == after