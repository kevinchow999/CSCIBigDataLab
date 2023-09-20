from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r"[\w']+")

class InvertedIndex(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer)
        ]

    def mapper(self, _, line):
        match = re.match(r'Document (\d+): (.+)', line)
        if match:
            doc, text = match.groups()
            words = WORD_RE.findall(text)
            for word in words:
                yield word, "Document " + doc

    def reducer(self, word, doc_ids):
        doc_ids = list(set(doc_ids))
        doc_ids = [doc.replace('Document', 'Document') for doc in doc_ids]
        yield word, ', '.join(doc_ids)

if __name__ == '__main__':
    InvertedIndex.run()
