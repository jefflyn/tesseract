# from googletrans import Translator
# translator = Translator()
# result = translator.translate("dog", src="en", dest="zh-cn")
# print(result.text)  # 输出：狗

from nltk.corpus import wordnet

# 获取单词的同义词集
synsets = wordnet.synsets("dog")
for syn in synsets:
    print(f"Definition: {syn.definition()}")
    print(f"Synonyms: {[lemma.name() for lemma in syn.lemmas()]}")