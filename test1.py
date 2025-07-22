import spacy
from collections import Counter
import re

# Import TextBlob for sentiment analysis with spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# --- GLOBAL SETUP ---
# Load the model and add the spacytextblob pipe for sentiment analysis
try:
    nlp = spacy.load("en_core_web_md")
    if 'spacytextblob' not in nlp.pipe_names:
        nlp.add_pipe('spacytextblob')
except OSError:
    print("Model 'en_core_web_md' not found. Please run 'python -m spacy download en_core_web_md'")
    exit()


# --- HELPER FUNCTIONS ---

def summarize_chat(doc, num_sentences=3):
    """Generates an extractive summary from the doc object."""
    keywords = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    word_freq = Counter(keywords)
    max_freq = max(word_freq.values(), default=1)
    norm_freq = {word: freq / max_freq for word, freq in word_freq.items()}
    
    sentence_scores = {sent: sum(norm_freq.get(word.text.lower(), 0) for word in sent) for sent in doc.sents}
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    
    summary_sentences = [sent.text.strip() for sent, score in sorted_sentences[:num_sentences]]
    return " ".join(summary_sentences)

def get_proper_keywords(doc, top_n=10):
    """Extracts high-quality keywords by combining POS, noun chunks, and entities."""
    pos_keywords = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'PROPN']]
    noun_chunks = [chunk.text.lower().replace("the ", "").replace("a ", "").replace("an ", "") for chunk in doc.noun_chunks]
    entities = [ent.text.lower() for ent in doc.ents if ent.label_ not in ['DATE', 'TIME', 'CARDINAL']]

    keyword_scores = Counter()
    keyword_scores.update(pos_keywords)
    for chunk in noun_chunks: keyword_scores[chunk] += 1
    for entity in entities: keyword_scores[entity] += 2

    final_keywords = keyword_scores.copy()
    for kw1 in keyword_scores:
        for kw2 in keyword_scores:
            if kw1 != kw2 and kw1 in kw2 and final_keywords[kw1] > 0:
                final_keywords[kw1] = 0
    
    return [kw for kw, count in final_keywords.most_common(top_n) if count > 0]

def find_questions_in_chat(doc):
    """Identifies and extracts questions from the chat."""
    questions = []
    for sent in doc.sents:
        if sent.text.strip().endswith('?'):
            # Remove speaker prefix like "Alice: " for cleaner output
            clean_question = re.sub(r'^\w+:\s*', '', sent.text.strip())
            questions.append(clean_question)
    return questions

def extract_contextual_details(doc):
    """Extracts structured details (people, orgs, topics, actions, dates)."""
    details = {
        "participants": set(), "organizations": set(), "topics": set(),
        "actions": set(), "dates_times": set()
    }
    for ent in doc.ents:
        if ent.label_ == "PERSON": details["participants"].add(ent.text)
        elif ent.label_ == "ORG": details["organizations"].add(ent.text)
        elif ent.label_ in ["DATE", "TIME"]: details["dates_times"].add(re.sub(r'^\s*the\s*', '', ent.text, flags=re.IGNORECASE))
    
    for chunk in doc.noun_chunks:
        topic = chunk.text.lower().replace("the ", "").replace("a ", "").replace("an ", "")
        details["topics"].add(topic)
        if chunk.root.head.pos_ == "VERB":
            details["actions"].add(f"{chunk.root.head.lemma_} {topic}")
            
    details["topics"] = {t for t in details["topics"] if t.lower() not in [p.lower() for p in details["participants"]]}
    return details

def generate_descriptive_context(details, doc):
    """Synthesizes extracted details into a descriptive paragraph."""
    context_sentences = []
    if details["participants"]:
        context_sentences.append(f"The conversation involves {', '.join(sorted(list(details['participants'])))}.")
    
    topics_and_orgs = sorted(list(details["topics"] | details["organizations"]), key=len, reverse=True)[:5]
    if topics_and_orgs:
        context_sentences.append(f"Key topics of discussion include {', '.join(topics_and_orgs)}.")
    
    polarity = doc._.blob.polarity
    sentiment_str = "neutral"
    if polarity > 0.2: sentiment_str = "positive"
    elif polarity < -0.2: sentiment_str = "negative"
    context_sentences.append(f"The overall tone is {sentiment_str}.")
    
    return " ".join(context_sentences) if context_sentences else "No specific context could be derived."


# --- MAIN ORCHESTRATOR ---

def full_chat_analysis(chat_log):
    """
    Performs a full analysis of a chat log and returns a structured dictionary.
    """
    full_text = " ".join(chat_log)
    doc = nlp(full_text)

    # Extract all pieces of information
    details = extract_contextual_details(doc)
    
    # Assemble the final report dictionary
    analysis_report = {
        "participants": sorted(list(details["participants"])),
        "questions": find_questions_in_chat(doc),
        "keywords": get_proper_keywords(doc, top_n=7),
        "descriptive_context": generate_descriptive_context(details, doc),
        "summary": summarize_chat(doc, num_sentences=3)
    }
    return analysis_report


# --- SCRIPT EXECUTION ---

if __name__ == "__main__":
    # Sample chat conversation
    sample_chat = [
        "Alice: Hey Bob, are we still on for the project meeting tomorrow at 10 AM?",
        "Bob: Hi Alice! Yes, absolutely. I've finished the initial draft for the Q3 report.",
        "Alice: Great! Did you include the sales figures from the new campaign with Acme Corp?",
        "Bob: I did. The results are looking very promising. I'll present them tomorrow.",
        "Charlie: I'll be joining too. I have some updates from the marketing team regarding the 'Project Phoenix' launch.",
        "Alice: Sounds good. Is everyone okay with the current agenda?"
    ]

    # Get the full analysis
    analysis = full_chat_analysis(sample_chat)

    # --- Print the formatted report ---
    print("📈 FULL CHAT ANALYSIS REPORT")
    print("="*30)

    # 1. Name of the peoples on chat
    print("\n## 1. Name of the peoples on chat")
    print(", ".join(analysis['participants']) if analysis['participants'] else "No participants identified.")

    # 2. What are the questions
    print("\n## 2. What are the questions")
    if analysis['questions']:
        for i, q in enumerate(analysis['questions'], 1):
            print(f"   {i}. {q}")
    else:
        print("   No questions were asked in the chat.")

    # 3. Keywords
    print("\n## 3. Keywords")
    print(", ".join(analysis['keywords']) if analysis['keywords'] else "No keywords found.")

    # 4. Context
    print("\n## 4. Context")
    print(analysis['descriptive_context'])

    # 5. Summary (A logical fifth point combining the core requests)
    print("\n## 5. Summary")
    print(analysis['summary'])
