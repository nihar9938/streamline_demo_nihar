import spacy
from collections import Counter
from string import punctuation

# Load the medium-sized English model from spacy
# This model includes vectors, part-of-speech tagging, and named entity recognition
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("Model 'en_core_web_md' not found. Please run 'python -m spacy download en_core_web_md'")
    exit()

def summarize_chat(chat_log, summary_sentences_count=3):
    """
    Summarizes a chat conversation and extracts context using spacy.

    Args:
        chat_log (list): A list of strings, where each string is a chat message.
        summary_sentences_count (int): The number of sentences to include in the summary.

    Returns:
        dict: A dictionary containing the 'summary' and 'context'.
    """
    if not chat_log:
        return {"summary": "The chat is empty.", "context": {}}

    # 1. Combine chat messages and process with spacy
    full_text = " ".join(chat_log)
    doc = nlp(full_text)

    # 2. Word Frequency Calculation (for summarization)
    # Get all tokens that are not stop words or punctuation
    keywords = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(keywords)
    max_freq = max(word_freq.values(), default=1)

    # Normalize frequencies
    norm_freq = {word: freq / max_freq for word, freq in word_freq.items()}

    # 3. Sentence Scoring
    sentence_scores = {}
    for sent in doc.sents:
        # Score a sentence by summing the normalized frequencies of its words
        score = sum(norm_freq.get(word.text.lower(), 0) for word in sent)
        sentence_scores[sent] = score

    # 4. Generate Summary
    # Get the top N sentences with the highest scores
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    top_sentences = [sent.text for sent, score in sorted_sentences[:summary_sentences_count]]
    summary = " ".join(top_sentences)

    # 5. Extract Context
    # Named Entity Recognition (People, Organizations, Dates, etc.)
    entities = {
        ent.label_: list(set([e.text for e in doc.ents if e.label_ == ent.label_]))
        for ent in doc.ents
    }

    # Key Topics (using noun chunks)
    topics = [chunk.text for chunk in doc.noun_chunks]
    top_topics = [item for item, count in Counter(topics).most_common(5)]

    context = {
        "key_entities": entities,
        "main_topics": top_topics
    }

    return {"summary": summary, "context": context}

# --- Example Usage ---
if __name__ == "__main__":
    # Sample chat conversation
    sample_chat = [
        "Alice: Hey Bob, are we still on for the project meeting tomorrow at 10 AM?",
        "Bob: Hi Alice! Yes, absolutely. I've finished the initial draft for the Q3 report.",
        "Alice: Great! Did you include the sales figures from the new campaign with Acme Corp?",
        "Bob: I did. The results are looking very promising. I'll present them tomorrow.",
        "Charlie: I'll be joining too. I have some updates from the marketing team regarding the 'Project Phoenix' launch.",
        "Alice: Perfect, Charlie. See you both at the conference room. Don't forget your laptops."
    ]

    # Get the summary and context
    chat_analysis = summarize_chat(sample_chat, summary_sentences_count=3)

    # Print the results
    print("💬 CHAT ANALYSIS")
    print("=" * 20)

    print("\n## 📝 Summary")
    print(chat_analysis['summary'])

    print("\n" + "-" * 20 + "\n")

    print("## CONTEXT")
    print("\n**Key Entities:**")
    for entity_type, entity_list in chat_analysis['context']['key_entities'].items():
        print(f"- {entity_type}: {', '.join(entity_list)}")

    print("\n**Main Topics:**")
    for topic in chat_analysis['context']['main_topics']:
        print(f"- {topic}")

