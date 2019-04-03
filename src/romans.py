class Romans:

    def __init__(self):
        self.mappings = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

    def to_dec(self, roman):
        result = 0
        skip = False

        for i in range(0, len(roman)):
            if skip:
                skip = False
                continue
            val1 = self.mappings[roman[i]]
            if i + 1 < len(roman):
                val2 = self.mappings[roman[i + 1]]
                if val1 >= val2:
                    result += val1
                else:
                    result += val2 - val1
                    skip = True
            else:
                result += val1

        return result
