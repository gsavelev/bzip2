class BWT:
    def transform(self, s):
        rotations = self.rotate(s)
        origin_idx, last_column = self.sort_in_lex(rotations, s)
        return origin_idx, last_column

    def rotate(self, s):
        rotations = []
        letters = [*s]
        for i in range(len(letters)):
            rotation = s[-1] + s[:-1]
            rotations.append(rotation)
            s = rotation
        return rotations

    def sort_in_lex(self, rotations, s):
        last_column = ''
        rotations = sorted(rotations)
        for i in range(len(rotations)):
            if rotations[i] == s:
                origin_idx = i
            last_column += rotations[i][-1]
        return origin_idx, last_column

    def restoration(self, origin_idx, last_column):
        # TODO restore origin sting
        pass