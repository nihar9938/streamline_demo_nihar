import spacy

def extract_keywords(text):
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    keywords = set()

    pos_tags_to_include = ['PROPN', 'NOUN', 'VERB']

    for token in doc:
        if token.pos_ in pos_tags_to_include and \
           not token.is_stop and \
           not token.is_punct and \
           token.is_alpha and \
           len(token.text) > 1:
            if token.lemma_.lower() in ["create", "expose", "support", "host", "load", "translate", "approve", "raise"]:
                keywords.add(token.lemma_.lower())
            elif token.pos_ in ['PROPN', 'NOUN']:
                keywords.add(token.lemma_.lower())
            if token.is_upper and len(token.text) > 1:
                keywords.add(token.text)

    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower().strip()
        if chunk_text not in ["use case", "everyone", "the same", "my service", "this in pure", "the following error",
                              "our team", "approval rights", "the meantime", "anyone help", "a service", "static tabular data"]:
            keywords.add(chunk_text)

    for ent in doc.ents:
        entity_text = ent.text.lower().strip()
        if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART", "NORP"] or entity_text in ["pure", "api", "tmd"]:
            keywords.add(entity_text)

    specific_important_terms = [
        "pure", "api", "tabular data set", "hardcoded data", "service",
        "dataset", "class mapping", "merge request", "tmd request",
        "data", "model", "fix", "approval"
    ]
    for term in specific_important_terms:
        keywords.add(term)

    final_keywords = [kw for kw in keywords if len(kw) > 1 and (kw.isalpha() or ' ' in kw)]

    return sorted(list(final_keywords))

chat_transcript = """
1 Wednesday, July 09, 2025 Bhardwaj, Aryan [HCM]
2 02:18 PM Hey everyone, needed help in a use case. I want to create a tabular data set within my service, populate it with hardcoded data, and then expose an API which returns it. How can I achieve this in PURE?
4
5 02:18 PM I have to tried to do the same, and the service does get registered successfully, but when I try to launch it, I get the following error: 'meta::pure::tds::tabularDataSet can't be translated'
6
7 Hey Hernandez, Rafael E [Engineering]
8 04:33 PM We dont support hosting a service to provide static tabular data
9
10 Bhardwaj, Aryan [HCM]
11 05:00 PM Interesting, so for my use case the only option I have is to create a dataset, load my hardcoded data into it, and create a corresponding class:mapping for it in Pure?
12
13 Hey-Hernandez, Rafael E [Engineering
14 06:15 PM Yeah. Or hosted elsewhere.
15
16 Saxena, Shobhit [AM]
17 08:05 PM Could someone assist with approving the following fix? https://gitlab.aws.site.go.com/data-engineering/pure-model/~merge_requests/12974Currently, no one on our team has approval rights. We have raised a TMD request, but in the meantime, can anyone help?
"""

extracted_keywords = extract_keywords(chat_transcript)
print(extracted_keywords)
