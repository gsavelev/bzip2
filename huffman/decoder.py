class Node:
    def __init__(self, root=None, left_child=None, right_child=None):
        self.root = root
        self.left_child = left_child
        self.right_child = right_child


class HuffmanDecoder:
    def __init__(self, tree, alphabet, code):
        self.flat_tree = tree
        self.alphabet = alphabet
        self.code = code
        self.c = -1

    def decode(self) -> list:
        decoded, curr_code = list(), str()
        codes = self.read_tree()

        for i in range(len(self.code)):
            curr_code += self.code[i]
            for key, val in codes:
                if curr_code == val:
                    decoded.append(key)
                    curr_code = ''
                    continue

        return decoded

    def read_tree(self) -> list:
        array, s = self.dfs(self.flat_tree)
        return array

    def dfs(self, s: str, code=''):
        if s[0] == '0':
            l, s = self.dfs(s[1:], code + '0')
            r, s = self.dfs(s, code + '1')
            return [*l, *r], s

        if s[0] == '1':
            self.c += 1
            return [(self.alphabet[self.c], code)], s[1:]
