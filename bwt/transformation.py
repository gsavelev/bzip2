class BWT:
    def transform(self, s: str) -> list:
        last_col = self.shift(s)
        return last_col

    def create_suffix_array(self, s: str) -> list:
        suff_num = []
        suff_arr = []
        for i in range(len(s)):
            suff_num.append((s[i:], i))
        suff_num.sort(key=lambda x: x[0])
        for s in suff_num:
            num = s[1]
            suff_arr.append(num)
        return suff_arr

    def shift(self, s: str) -> list:
        last_col = []
        # add STX and ETX symbols to the input string
        stx = '\002'
        etx = '\003'
        assert stx not in s and etx not in s
        s = stx + s + etx

        suff_arr = self.create_suffix_array(s)
        n = len(suff_arr)
        for i in range(n):
            last_char = s[(suff_arr[i] - 1 + n) % n]  # find the lact char of each rotation
            last_col.append(last_char)

        return last_col

    def mark(self, col: list, n: int) -> list:
        counter = dict()
        marked_col = []
        for i in range(n):
            sym = col[i]
            if sym not in counter.keys():
                counter[sym] = 0
            counter[sym] += 1
            marked_col.append((sym, counter[sym]))
        return marked_col

    def undo_transform(self, bwt_str: list) -> str:
        origin_str = ''
        n = len(bwt_str)
        bwt_str_sorted = sorted(bwt_str)  # first column of BWT matrix

        first_col = self.mark(bwt_str_sorted, n)
        last_col = self.mark(bwt_str, n)

        j = 0
        while j < n:
            # https://www.youtube.com/watch?v=DqdjbK68l3s
            if j == 0:
                k = 0
            (sym, i) = last_col[k][0], last_col[k][1]
            origin_str = sym + origin_str
            k = first_col.index((sym, i))
            j += 1

        return origin_str.rstrip('\003').strip('\002')


if __name__ == '__main__':
    bwt = BWT()
    before = 'abacaba'
    after = bwt.transform(before)
    undo_after = bwt.undo_transform(after)
    assert before == undo_after