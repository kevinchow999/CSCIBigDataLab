from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"[\w]+")

STOP_WORDS = ['the', 'and', 'of', 'a', 'to', 'in', 'is', 'it']
class WordCountStopWords(MRJob):

    def mapper(self, _, line):
        words = WORD_RE.findall(line)
        yield from ((word, 1) for word in words if word not in STOP_WORDS)

if __name__ == '__main__':
    WordCountStopWords.run()
