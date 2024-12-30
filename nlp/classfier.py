from collections import defaultdict

import nltk
from nltk.corpus import wordnet

# 确保 NLTK 数据已下载
nltk.download('wordnet')


class WordClassifier:
    def __init__(self, words):
        """
        初始化分类工具类
        :param words: list of str，待分类的单词列表
        """
        self.words = words

    def classify_by_length(self):
        """
        按长度分类单词
        :return: dict，键为长度，值为单词列表
        """
        length_dict = defaultdict(list)
        for word in self.words:
            length_dict[len(word)].append(word)
        return dict(length_dict)

    def classify_by_alphabet(self):
        """
        按首字母分类单词
        :return: dict，键为首字母，值为单词列表
        """
        alphabet_dict = defaultdict(list)
        for word in self.words:
            alphabet_dict[word[0].lower()].append(word)
        return dict(alphabet_dict)

    def classify_by_part_of_speech(self):
        """
        按词性分类单词（基于 WordNet）
        :return: dict，键为词性，值为单词列表
        """
        pos_dict = defaultdict(list)
        for word in self.words:
            synsets = wordnet.synsets(word)
            if synsets:
                pos = synsets[0].pos()  # 使用第一个释义的词性
                pos_dict[pos].append(word)
            else:
                pos_dict['unknown'].append(word)
        return dict(pos_dict)

    def classify_by_semantics(self, category):
        """
        按语义分类单词（如动物、地点等）
        :param category: str，语义类别，例如 'animal' 或 'place'
        :return: list，属于该类别的单词列表
        """
        category_words = []
        for word in self.words:
            synsets = wordnet.synsets(word)
            for syn in synsets:
                if category.lower() in [lemma.name().lower() for lemma in syn.hypernyms()]:
                    category_words.append(word)
                    break
        return category_words


words = ["cat", "dog", "run", "house", "apple", "jump", "elephant"]

# 初始化分类工具
classifier = WordClassifier(words)

# 按长度分类
print("按长度分类:", classifier.classify_by_length())

# 按首字母分类
print("按首字母分类:", classifier.classify_by_alphabet())

# 按词性分类
print("按词性分类:", classifier.classify_by_part_of_speech())

# 按语义分类（动物类单词）
print("动物类单词:", classifier.classify_by_semantics("animal"))
