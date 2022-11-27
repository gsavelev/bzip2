class Node:
    def __init__(self, root=None, left_child=None, right_child=None):
        self.root = root
        self.left_child = left_child
        self.right_child = right_child


class HuffmanDecoder:
    def __init__(self, encoded_split: list):
        self.flat_tree = encoded_split[0]
        self.alphabet = encoded_split[1]
        self.code = encoded_split[2]
        self.make_tree_alphabet()

    def make_tree_alphabet(self):
        c = 0
        for i in range(len(self.flat_tree)):
            if self.flat_tree[i] == 1:
                self.flat_tree[i] = self.alphabet[c]
                c += 1

    def decode(self) -> str:
        decoded_str = str()
        curr_code = str()
        tree = self.build_tree(0)

        if isinstance(tree, str):
            code_dict = {tree: '0'}
        else:
            code_dict = self.traverse(tree, prefix=list(), code_dict=dict())

        for i in range(len(curr_code)):
            curr_code += curr_code[i]
            for key, val in code_dict.items():
                if curr_code == val:
                    decoded_str += key
                    curr_code = ''
                    continue

        return decoded_str

    def build_tree(self, i):
        if i < len(self.flat_tree):
            return Node(root=self.flat_tree[i],
                        left_child=self.build_tree((i + 1) * 2 - 1),
                        right_child=self.build_tree((i + 1) * 2))

    def traverse(self, root, prefix, code_dict) -> dict:
        # TODO restore code dict
        if isinstance(root, str):
            code_dict[root] = ''.join(prefix)
            return code_dict

        prefix.append('0')
        code_dict = self.traverse(root.left_child, prefix, code_dict)
        prefix.pop()

        prefix.append('1')
        code_dict = self.traverse(root.right_child, prefix, code_dict)
        prefix.pop()

        return code_dict


if __name__ == '__main__':
    flat_tree = [0, 0, 0, 0, 1, 1, 1, 1, 1]
    alphabet = ['E', 'C', 'A', 'B', 'D']
    code = None
    h = HuffmanDecoder([flat_tree, alphabet, code])
    h.decode()