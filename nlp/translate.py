# from googletrans import Translator
# translator = Translator()
# result = translator.translate("dog", src="en", dest="zh-cn")
# print(result.text)  # 输出：狗

# from nltk.corpus import wordnet
#
# # 获取单词的同义词集
# synsets = wordnet.synsets("dog")
# for syn in synsets:
#     print(f"Definition: {syn.definition()}")
#     print(f"Synonyms: {[lemma.name() for lemma in syn.lemmas()]}")


import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The quick brown fox jumps over the lazy dog.")
for token in doc:
    print(f"Word: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")