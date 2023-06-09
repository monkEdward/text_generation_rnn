from collections import Counter
import torch


class Dataset(torch.utils.data.Dataset):

    def __init__(self,TRAIN_DATA_PATH):
        self.TRAIN_DATA_PATH=TRAIN_DATA_PATH
        self.sequence_length = 40
        self.words = self.load_words(TRAIN_DATA_PATH)
        self.uniq_words = self.get_uniq_words()     # vocabulary
        
        self.index_to_word = {index: word for index, word in enumerate(self.uniq_words)}
        self.word_to_index = {word: index for index, word in enumerate(self.uniq_words)}

        self.words_indexes = [self.word_to_index[w] for w in self.words]

    def load_words(self,TRAIN_DATA_PATH):
        text = open(TRAIN_DATA_PATH, 'rb').read().decode(encoding='utf-8')
        return text.split(' ')

    def get_uniq_words(self):
        word_counts = Counter(self.words)
        return sorted(word_counts, key=word_counts.get, reverse=True)

    def __len__(self):
        return len(self.words_indexes) - self.sequence_length

    def __getitem__(self, index):
        return (
            torch.tensor(self.words_indexes[index:index+self.sequence_length]),
            torch.tensor(self.words_indexes[index+1:index+self.sequence_length+1]),
        )
