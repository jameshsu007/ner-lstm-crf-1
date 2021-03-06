from data_utils import get_trimmed_glove_vectors, load_vocab, \
    get_processing_word, CoNLLDataset
from model import NERModel
from config import Config

config = Config()

vocab_words = load_vocab(config.words_filename)  # words idx
vocab_tags = load_vocab(config.tags_filename)  # tags idx
vocab_chars = load_vocab(config.chars_filename)  # char idx

processing_word = get_processing_word(vocab_words, vocab_chars)
processing_tag = get_processing_word(vocab_tags)

embeddings = get_trimmed_glove_vectors(config.trimmed_filename)

dev = CoNLLDataset(filename=config.dev_filename,
                   processing_word=processing_word,
                   processing_tag=processing_tag,
                   max_iter=config.max_iter)
test = CoNLLDataset(filename=config.test_filename,
                    processing_word=processing_word,
                    processing_tag=processing_tag,
                    max_iter=config.max_iter)
train = CoNLLDataset(filename=config.train_filename,
                     processing_word=processing_word,
                     processing_tag=processing_tag,
                     max_iter=config.max_iter)

model = NERModel(config=config,
                 embeddings=embeddings,
                 ntags=len(vocab_tags),
                 nchars=len(vocab_chars))

model.train(train, dev, vocab_tags)
model.test(test, vocab_tags)
model.interactive_shell(vocab_tags, processing_word)
