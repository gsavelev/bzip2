import string


class MTF:
    def __init__(self):
        self.alphabet = [chr(i) for i in range(128)]

    def transform(self, s: str) -> list:
        transformed = []
        for i in range(len(s)):
            s_idx = self.alphabet.index(s[i])
            transformed.append(s_idx)
            self.alphabet.insert(0, self.alphabet[s_idx])
            del self.alphabet[s_idx + 1]  # + 1 here to compensate insert above
        return transformed

    def undo_transform(self, transformed: list) -> str:
        origin_str = ''
        for i in transformed:
            origin_str += self.alphabet[i]
            self.alphabet.insert(0, self.alphabet[i])
            del self.alphabet[i + 1]  # + 1 here to compensate insert above
        return origin_str
