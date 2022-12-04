class Node:
    def __init__(self, root=None, left_child=None, right_child=None):
        self.root = root
        self.left_child = left_child
        self.right_child = right_child


class HuffmanDecoder:
    def __init__(self, encoded_split: list):
        self.flat_tree = [c for c in encoded_split[0]]
        self.alphabet = [c for c in encoded_split[1]]
        self.code = encoded_split[2]

    def make_tree_alphabet(self):
        c = 0
        for i in range(len(self.flat_tree)):
            if self.flat_tree[i] == '1':
                self.flat_tree[i] = str(self.alphabet[c])
                c += 1

    def decode(self) -> str:
        self.make_tree_alphabet()  # in this task alphabet is list of ints

        decoded = list()
        curr_code = str()
        tree = self.build_tree(0)
        code_dict = self.traverse(tree, prefix=list(), code_dict=dict())

        for i in range(len(self.code)):
            curr_code += self.code[i]
            for key, val in code_dict.items():
                if curr_code == val:
                    decoded.append(int(key))
                    curr_code = ''
                    continue

        return decoded

    def build_tree(self, i):
        # FIXME build tree not in right way
        if i < len(self.flat_tree):
            return Node(root=self.flat_tree[i],
                        left_child=self.build_tree((i + 1) * 2 - 1),
                        right_child=self.build_tree((i + 1) * 2))

    def traverse(self, root, prefix, code_dict) -> dict:
        if root.left_child is None and root.right_child is None:
            code_dict[root.root] = ''.join(prefix)
            return code_dict
        else:
            prefix.append('0')
            code_dict = self.traverse(root.left_child, prefix, code_dict)
            prefix.pop()

            prefix.append('1')
            code_dict = self.traverse(root.right_child, prefix, code_dict)
            prefix.pop()

        return code_dict
