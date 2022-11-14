class HuffmanDecoder:
    def __init__(self, code_dict: dict):
        self.code_dict = code_dict

    def decode(self, code_str) -> str:
        decoded_str = str()
        code = str()
        for i in range(len(code_str)):
            code += code_str[i]
            for key, val in self.code_dict.items():
                if code == val:
                    decoded_str += key
                    code = ''
                    continue
        return decoded_str
