import spacy

nlp = spacy.load("en_core_web_sm")


# doc = nlp("The quick brown fox jumps over the lazy dog.")
# for token in doc:
#     print(f"Word: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")

def get_token_map(text):
    doc = nlp(text)
    result_map = {}
    for token in doc:
        print(f"Word: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}")
        result_map[token.text] = {'pos': token.pos_, 'lemma': token.lemma_}
    return result_map

if __name__ == '__main__':
    print(get_token_map('hello china China Hello'))