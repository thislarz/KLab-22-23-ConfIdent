
class OrdinalNumbers(object):
    def __init__(self):
        self.ordinal_list = [
            'first', 'second', 'third', 'fourth', 'fifth',
            'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
            'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth',
            'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth', 'twenty',
            'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'
        ]

    def get_ordnial(self, number: int):
        return self.ordinal_list[int-1]

    def get_ordinal_list(self):
        return self.ordinal_list
