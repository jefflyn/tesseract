import spacy

nlp = spacy.load("en_core_web_sm")


# doc = nlp("The quick brown fox jumps over the lazy dog.")
# for token in doc:
#     print(f"Word: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")

def get_token_map(text):
    doc = nlp(text)
    # 打印所有命名实体及其类型
    for ent in doc.ents:
        print(ent.text, ent.label_)
    result_map = {}
    for token in doc:
        print(f"Word: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")
        result_map[token.text] = {'pos': token.pos_, 'lemma': token.lemma_}
    return result_map

if __name__ == '__main__':
    print(get_token_map('Barack Obama was born in Hawaii and worked at the White House.'))