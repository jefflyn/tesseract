import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet

# 下载必要的数据
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')


# 定义一个函数将 nltk 的 POS 标注映射到 WordNet 格式
def nltk_pos_to_wordnet(nltk_pos):
    if nltk_pos.startswith('J'):
        return wordnet.ADJ
    elif nltk_pos.startswith('V'):
        return wordnet.VERB
    elif nltk_pos.startswith('N'):
        return wordnet.NOUN
    elif nltk_pos.startswith('R'):
        return wordnet.ADV
    else:
        return None

#
# # 示例文本
# text = "The quick brown fox jumps over the lazy dog."
#
# # 分词
# words = word_tokenize(text)
#
# # 获取词性标注
# tagged_words = pos_tag(words)
#
# # 使用 WordNet 映射
# for word, nltk_pos in tagged_words:
#     wordnet_pos = nltk_pos_to_wordnet(nltk_pos)
#     if wordnet_pos:
#         synsets = wordnet.synsets(word, pos=wordnet_pos)  # 获取特定词性的同义词集
#         if synsets:
#             definition = synsets[0].definition()  # 获取第一个同义词集的定义
#             print(f"Word: {word}, POS: {wordnet_pos}, Definition: {definition}")
#         else:
#             print(f"Word: {word}, POS: {wordnet_pos}, No Synsets Found")
#     else:
#         print(f"Word: {word}, POS: {nltk_pos}, Not Mapped to WordNet")


# 获取单词的同义词集
# synsets = wordnet.synsets("shit")
# for syn in synsets:
#     print(f"Definition: {syn.definition()}")
#     print(f"Synonyms: {[lemma.name() for lemma in syn.lemmas()]}")

# 获取单词的同义词集
def get_synset(word):
    synsets = wordnet.synsets(word)
    result = ''
    for n in range(0, len(synsets)):
        syn = synsets[n]
        # print(f"Definition: {syn.definition()}")
        # print(f"Synonyms: {[lemma.name() for lemma in syn.lemmas()]}")
        result = (result + 'Definition-' + str(n + 1) + ': ' + syn.definition() + '\n'
                  + '  --Synonyms: ' + str([lemma.name() for lemma in syn.lemmas()]) + '\n')
    return result


if __name__ == '__main__':
    print(get_synset('china'))
