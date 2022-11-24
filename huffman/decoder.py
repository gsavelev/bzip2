class Node:
    def __init__(self, root, left_child, right_child):
        self.root = root
        self.left_child = left_child
        self.right_child = right_child

    def is_leaf(self):
        return self.left_child is None


class HuffmanDecoder:
    def __init__(self, encoded_split: list):
        self.flat_tree = encoded_split[0]
        self.alphabet = encoded_split[1]
        self.code = encoded_split[2]

    def decode(self) -> str:
        decoded_str = str()
        curr_code = str()
        code_dict = self.unfold_tree()

        for i in range(len(curr_code)):
            curr_code += curr_code[i]
            for key, val in code_dict.items():
                if curr_code == val:
                    decoded_str += key
                    curr_code = ''
                    continue

        return decoded_str

    def unfold_tree(self, index=0) -> dict:
        # TODO pass flatten tree and restore code_dict
        # https://stackoverflow.com/questions/759707/efficient-way-of-storing-huffman-tree
        pass
