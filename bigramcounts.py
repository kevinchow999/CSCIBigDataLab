from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r"[\w']+")

class CountBigrams(MRJob):
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer)
        ]

    def mapper(self, _,line):
        words = WORD_RE.findall(line)
        for i in range(len(words) - 1):
            bigram = f"{words[i]},{words[i + 1]}"
            yield bigram, 1

    def reducer(self, bigram, counts):
        total_count = sum(counts)
        yield bigram, total_count

if __name__ == '__main__':
    CountBigrams.run()
