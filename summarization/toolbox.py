from nltk.tokenize import sent_tokenize, word_tokenize
from numpy import log2

class WordDistribution:
    
    def __init__(self, document, smoothing=1, stop_words=set([]), vocabulary=None):
        self.vocabulary = vocabulary
        self.document = document
        self.stop_words = stop_words
        self.parse_sentences()
        self.count_words()
        self.calculate_distribution(smoothing)
        
    def parse_sentences(self):
        sentences = sent_tokenize(self.document)
        self.sent_tokens = [word_tokenize(sentence) for sentence in sentences]
    
    def count_words(self):
        self.word_counts = {}
        self.total = 0
        for word in (word for sentence in self.sent_tokens for word in sentence):
            if self.vocabulary is not None and word not in self.vocabulary:
                continue
            if word in self.stop_words:
                continue
            if word not in self.word_counts:
                self.word_counts[word] = 0
            self.word_counts[word] += 1
            self.total += 1
        if self.vocabulary is None:
            self.vocabulary = set(self.word_counts.keys())
    
    def calculate_distribution(self, smoothing=1):
        # smoothing added to prevent cross entropy evaluating to infinity
        self.word_distribution = {}
        total_words = len(self.vocabulary)
        for word in self.vocabulary:
            count = self.word_counts.get(word, 0)
            self.word_distribution[word] = (float(count) + smoothing) / (self.total + smoothing * total_words)
            
    def cross_entropy(self, other_distribution):
        return sum(-other_distribution.word_distribution[key] * log2(self.word_distribution[key]) for key in self.vocabulary)
    
    def entropy(self):
        return sum(-p * log2(p) for p in self.word_distribution.values())
    
    def kl_divergence(self, other_distribution):
        return self.cross_entropy(other_distribution) - other_distribution.entropy()