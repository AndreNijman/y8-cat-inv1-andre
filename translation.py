import triples

class Translation:
    def Triple_Finder(self, distance, direction):
        reverse_sorted=sorted(triples.triples, reverse=True, key=lambda element: element[2])
        result = list(filter(lambda i: i[2] <= distance, reverse_sorted))[0]
        result1, result2 = result[0], result[1]
        return result1, result2, direction

    def Triple_to_Movement(self, triple, direction):
        translation = [
           [1, 1, True],
           [1, 1, False],           
           [-1, 1, False],
           [-1, 1, True],
           [-1, -1, True],
           [-1, -1, False],
           [1, -1, False],
           [1, -1, True],
        ]
        current = translation[direction - 1]
        reverse = current[2]
        if not reverse:
            move1 = triple[0] * current[0]
            move2 = triple[1] * current[1]
        else:
            move1 = triple[1] * current[0] # 3
            move2 = triple[0] * current[1] # 4
        return move1, move2