import sys
from functools import partial


class BWT:
    def radix_sort(self, val, key, step=0):
        if len(val) < 2:
            for value in val:
                yield value
            return

        batches = {}
        for value in val:
            batches.setdefault(key(value, step), []).append(value)

        for k in sorted(batches.keys()):
            for r in self.radix_sort(batches[k], key, step + 1):
                yield r

    def get_sym(self, text, val, step):
        return text[(val + step) % len(text)]

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

    def transform(self, text: str) -> list:
        sys.setrecursionlimit(2000)

        stx, etx = chr(2), chr(3)
        if stx not in text:
            text = stx + text
        if etx not in text:
            text = text + etx

        bwt_list = list()

        for i in self.radix_sort(range(len(text)), partial(self.get_sym, text)):
            bwt_list.append(text[i - 1])

        return bwt_list

    def undo_transform(self, bwt_list: list) -> str:
        origin_str = ''
        stx, etx = chr(2), chr(3)
        n = len(bwt_list)

        first_col = self.mark(sorted(bwt_list), n)
        last_col = self.mark(bwt_list, n)

        j = 0
        while j < n:
            # https://www.youtube.com/watch?v=DqdjbK68l3s
            if j == 0:
                k = 0
            (sym, i) = last_col[k][0], last_col[k][1]
            origin_str = sym + origin_str
            k = first_col.index((sym, i))
            j += 1

        return origin_str.rstrip(f'{etx}').strip(f'{stx}')
