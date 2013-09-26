import sys
import re
from collections import defaultdict, Counter
import random
from iter_prefix import iter_prefix

terminators = '([?.!])'


class MarkovWords(object):
    def __init__(self, text, max_len=2):
        self.length = max_len
        self.word_tables = []
        # Create a word table for each tuple length
        for i in range(0, max_len):
            self.word_tables.append(self.create_table(text, i))

    def create_table(self, text, prefix_len):
        # Break up text based on line enders
        sentences = re.findall('([^.!?]*)([.?!])', text)
        # Parse out the text and the enders separately
        sentences = map(lambda x: (x[0].strip(), x[1]), sentences)
        # Ignore empty sentences
        sentences = filter(lambda x: x[0], sentences)
        word_table = defaultdict(Counter)
        for sentence, term in sentences:
            # Split the sentence into words
            words = map(lambda x: x.lower(), sentence.split())
            # Break the words into prefix_len-long groups
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
