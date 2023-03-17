import resource
import sys
from functools import partial


class BWT:
    def radix_sort(self, vals, key, step=0):
        if len(vals) < 2:
            for val in vals:
                yield val
            return

        batches = {}
        for val in vals:
            batches.setdefault(key(val, step), []).append(val)

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

    def transform(self, text: bytes) -> list:
        sys.setrecursionlimit(10**6)

        bwt_list, last_idx, eof = list(), None, text[-1]

        for i in self.radix_sort(range(len(text)), partial(self.get_sym, text)):
            sym = chr(text[i - 1]).encode(encoding='latin-1')
            if i == len(text) - 1:
                last_idx = len(bwt_list)
            bwt_list.append(sym)

        return bwt_list, last_idx, eof

    def undo_transform(
            self, bwt_list: list, last_idx: int, eof: int) -> bytearray:
        origin = bytearray()
        n = len(bwt_list)

        first_col = self.mark(sorted(bwt_list), n)
        last_col = self.mark(bwt_list, n)

        j = 0
        while j < n - 1:
            # https://youtu.be/DqdjbK68l3s
            if j == 0:
                if last_idx:
                    k = last_idx
                else:
                    raise ValueError('Last origin symbol index not found!')
            sym, i = last_col[k][0], last_col[k][1]
            origin[0:0] = sym
            k = first_col.index((sym, i))
            j += 1

        origin.append(eof)

        return origin
