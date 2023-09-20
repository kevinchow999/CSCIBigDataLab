from mrjob.job import MRJob
import re

# Splitting words
WORD_RE = re.compile(r"[\w]+")

class UniqueWordCount(MRJob):

    def mapper(self, _, line):
        words = WORD_RE.findall(line) #Finding all words on a line
        for word in words:
            yield word, 1 # Mapping each key with a value of 1 

if __name__ == '__main__':
    UniqueWordCount.run()