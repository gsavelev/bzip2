class BWT:
    def transform(self, s):
        shifts = self.shift(s)
        origin_idx, last_column = self.lex_sort(shifts, s)
        return origin_idx, last_column

    def shift(self, s):
        # TODO change storing in big matrix to how many units shifted
        #  https://www.geeksforgeeks.org/burrows-wheeler-data-transform-algorithm/
        #  https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform
        #  I need to use suffix data structure
        #  and add EOF sym
        shifts = []
        letters = [*s]
        for i in range(len(letters)):
            rotation = s[-1] + s[:-1]
            shifts.append(rotation)
            s = rotation
        return shifts

    def lex_sort(self, shifts, s):
        last_column = ''
        rotations = sorted(shifts)
        for i in range(len(rotations)):
            if rotations[i] == s:
                origin_idx = i
            last_column += rotations[i][-1]
        return last_column, origin_idx

    def undo(self, bwt_str, origin_idx):
        # TODO do not n^2 way
        #  https://www.geeksforgeeks.org/inverting-burrows-wheeler-transform/
        #  https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform
        n = len(bwt_str)
        shifts = [""] * n
        for i in range(n):  # restore shifts
            shifts = sorted(bwt_str[i] + shifts[i] for i in range(n))  # add one column of shift
        origin_str = shifts[origin_idx]
        return origin_str


if __name__ == '__main__':
    bwt = BWT()
    before = 'abacaba'
    after, i = bwt.transform(before)
    after = bwt.undo(after, i)
    assert before == after