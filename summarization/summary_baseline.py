from numpy import mean
def calculate_frequencies(sent_tokens):
    document = []
    for sent in sent_tokens:
        document += sent
        
    max_freq, min_freq = .9, .1
    counts = {}
    for word in document:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
            
    max_c = float(max(counts.values()))
    freq = {}
    for word, count in counts.items():
        f =  count / max_c
        if f > min_freq and f < max_freq:
            freq[word] = f
    return freq

def score_sentence(sentence, frequencies):
    scores = []
    if len(sentence) < 50:
        for word in sentence:
            if word in frequencies:
                scores.append(frequencies[word])
    return mean(scores) if len(scores) > 0 else 0

def score_sentences(sent_tokens, word_counts):
    scores = {}
    for i, sentence in enumerate(sent_tokens):
        scores[i] = score_sentence(sentence, word_counts)
    return scores