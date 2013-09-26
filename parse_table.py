import sys
import re
from collections import defaultdict, Counter
import random

terminators = '([?.!])'


def iterpairs(l):
    return ((pre[0], n) for pre, n in iter_prefix(l))


def iter_prefix(l, prefix_len=1):
    return (
        (
            tuple(l[i + j] for j in range(prefix_len)),
            l[i + prefix_len]
        ) for i in range(len(l) - prefix_len)
    )


class MarkovWords(object):
    def __init__(self, text, max_len=2):
        self.length = max_len
        self.word_tables = []
        for i in range(0, max_len):
            self.word_tables.append(self.create_table(text, i))

    def create_table(self, text, prefix_len):
        sentences = filter(lambda x: x[0], map(lambda x: (x[0].strip(), x[1]), re.findall('([^.!?]*)([.?!])', text)))
        word_table = defaultdict(Counter)
        for sentence, term in sentences:
            words = map(lambda x: x.lower(), sentence.split())
            for pair in iter_prefix(words, prefix_len):
                prefix, n = pair
                word_table[prefix][n] += 1
            if words:
                word_table[tuple(words[-prefix_len:])][term] += 1
        return word_table

    def get_sentence(self):
        prefix = random.choice(self.word_tables[-1].keys())
        words = [" ".join(prefix).capitalize()]
        while True:
            for i in range(-self.length + 1, 1):
                range_len = sum(self.word_tables[-i][prefix[i:]].values())
                if range_len > 0:
                    roll = random.randrange(range_len)
                    for new, cnt in self.word_tables[-i][prefix[i:]].iteritems():
                        if cnt >= roll:
                            if re.match(terminators, new):
                                words[-1] = words[-1] + new
                                return " ".join(words)
                            else:
                                prefix = tuple(list(prefix[1:]) + [new])
                                words.append(new)
                            break
                        roll -= cnt
                    break
            


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        text = f.read()
    mk = MarkovWords(text)
    print mk.get_sentence()
