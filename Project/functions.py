import re
from spellchecker import SpellChecker
import pandas as pd
from pathlib import Path
import statistics 
import spacy
from nltk import pos_tag, word_tokenize
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse



# read file
def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

# function that counts the number of sentences, and provides a score
def count_sentences(essay, nlp):
    doc = nlp(essay)
    sentence_count = 0
    for sent in doc.sents: # for each instance that spaCy tokenizes
        finite_verbs = [token for token in sent if token.tag_ in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ") and token.dep_ != "aux"]
        if finite_verbs:
            sentence_count += 1
    if sentence_count > 25:
        score = 5
    elif sentence_count > 20:
        score = 4
    elif sentence_count > 15:
        score = 3
    elif sentence_count > 10:
        score = 2
    else:
        score = 1
    return score

# function used to get the median counts for high and low, part of corpus analysis
def median_corpus_counts(nlp):
    df = pd.read_csv('essays_dataset/index.csv', delimiter=';')
    sentence_counts = {'high': [], 'low': []}
    for index, row in df.iterrows():
        file_path = f"essays_dataset/essays/{row['filename']}"
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as file:
                essay_text = file.read()
                sentence_count = count_sentences(essay_text, nlp)
                sentence_counts[row['grade']].append(sentence_count) 
        else:
            print(f"File not found: {file_path}")
    median_high = statistics.median(sentence_counts['high']) if sentence_counts['high'] else 0
    median_low = statistics.median(sentence_counts['low']) if sentence_counts['low'] else 0

    print(f"Median Sentence Count for High Essays: {median_high}")
    print(f"Median Sentence Count for Low Essays: {median_low}")

# function that scores the subject verb agreement (e.g. plurality)
def score_subject_verb_agreement(essay, nlp):
    if not essay.strip():  # Check for empty essays
        return 0 
    doc = nlp(essay)
    agreements = 0
    total = 0
    for token in doc:
        if "subj" in token.dep_:  # check if word is a subject
            # Find the main verb in the sentence
            verbs = [child for child in token.head.children if child.pos_ == "VERB"]
            main_verb = verbs[0] if verbs else None
            if main_verb:
                total += 1
                # check the tags for the tokens, and see if they're in agreement
                subject_agreement = "SINGULAR" if token.tag_ in {"NN", "NNP"} else "PLURAL"
                verb_agreement = "SINGULAR" if main_verb.tag_ in {"VBZ", "VBP"} else "PLURAL"
                if subject_agreement == verb_agreement:
                    agreements += 1
                # print(f'{(token, main_verb)}, {subject_agreement == verb_agreement}')
    agreement_ratio = (agreements / total) if total > 0 else 0
    # Return a score based on the ratio
    score = 0
    if agreement_ratio > 0.75:
        score = 4
    elif agreement_ratio > 0.50:
        score= 3
    elif agreement_ratio > 0.25:
        score= 2
    else:
        score= 1
    return score

# helper function for checking main verbs, use for corpus analysis to see sentence structure 
def check_main_verbs(essay, nlp):
    doc = nlp(essay)
    total_sentences = 0
    sentences_with_main_verbs = 0

    for sent in doc.sents:
        total_sentences += 1
        # Check for a main verb in the sentence, which isn't an auxiliary verb
        if any(token.pos_ == 'VERB' and token.dep_ not in {'aux', 'auxpass'} for token in sent):
            sentences_with_main_verbs += 1

    return sentences_with_main_verbs, total_sentences

# function that analyzes verb-tense errors and errors with auxiliaries 
def analyze_verb_errors(essay, nlp):
    # Tokenize and POS tag using NLTK
    nltk_pos_tags = pos_tag(word_tokenize(essay))
    
    spacy_doc = nlp(essay)
    
    error_count = 0
    total_verbs = 0
    
    # Check for incorrect 'to be' followed by infinitival verb (to + base form)
    for i, pair in enumerate(nltk_pos_tags[:-1]):
        if pair[0].lower() == 'to' and nltk_pos_tags[i + 1][1] == 'VB':
            if i > 0 and nltk_pos_tags[i - 1][1] in {'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}:
                # If the 'to' follows another verb (that is not modal), might be an error
                error_count += 1
        
        # Count total verbs
        if pair[1].startswith('VB'):
            total_verbs += 1

    # Check tags for auxiliaries and verbs
    for token in spacy_doc:
        if token.pos_ == "AUX" and token.dep_ == "aux" and token.head.pos_ != "VERB":
            # If there is an auxiliary without a main verb, coul be an error
            error_count += 1
        if token.pos_ == "VERB" and token.dep_ == "ROOT":
            total_verbs += 1

    error_ratio = error_count / total_verbs if total_verbs > 0 else 0
    er = error_count / 30
    score = max(5 - int(er * 5), 1)
    return score

def spell_check(essay):
    spell = SpellChecker()
    words = re.findall(r'\b\w+\b', essay.lower()) 
    misspelled = spell.unknown(words)
    num_mistakes = len(misspelled)
    if num_mistakes > 20:
        return 4
    elif num_mistakes > 15:
        return 3
    elif num_mistakes > 10:
        return 2
    elif num_mistakes > 5:
        return 1
    else:
        return 0
    
def evaluate_syntactic_well_formedness(essay, nlp):
    doc = nlp(essay)
    errors = 0
    total_sentences = 0
    
    for sent in doc.sents:
        total_sentences += 1

        if not any(token.pos_ == 'VERB' and token.dep_ not in {'aux', 'auxpass'} for token in sent):
            errors += 1
        for token in sent:
            if token.dep_ == 'mark' and not (token.head.pos_ == 'VERB' and token.head.dep_ in {'advcl', 'csubj', 'ccomp'}):
                errors += 1
    
    error_ratio = errors / total_sentences if total_sentences > 0 else 1

    score = max(5 - int(error_ratio * 5), 1)
    return score



def evaluate_essay_coherence(essay, nlp):
    doc = nlp(essay)
    embeddings = []
    
    for sent in doc.sents:
        sent_vecs = [token.vector for token in sent if not token.is_stop and token.has_vector]
        if sent_vecs:
            embeddings.append(sparse.csr_matrix(np.mean(sent_vecs, axis=0)))
    
    if len(embeddings) > 1:
        sim_scores = cosine_similarity(sparse.vstack(embeddings))
        avg_sim = np.mean([sim_scores[i, i + 1] for i in range(len(embeddings) - 1)])
    else:
        avg_sim = 0  


    if avg_sim > 0.75:
        score = 5
    elif avg_sim > 0.60:
        score = 4
    elif avg_sim > 0.45:
        score = 3
    elif avg_sim > 0.30:
        score = 2
    else:
        score = 1
    
    return score