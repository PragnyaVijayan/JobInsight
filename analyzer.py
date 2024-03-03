import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline
import re


def analyze_job_description(job_description):
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(job_description)
    special_chars = r'[?.\'"&^()!|]'

    filtered_words = [
        word for word in words
        if (
            re.match('^[a-zA-Z]+$', word) and
            word.lower() not in stop_words and
            not re.search(special_chars, word)
        )
    ]
    # Use LLM to extract keywords
    nlp = pipeline("fill-mask", model="bert-base-uncased")
    masked_description = ' '.join([f'[MASK] {word} [MASK]' for word in filtered_words])
    predictions_list = nlp(masked_description)

    # Extracting keywords from LLM predictions and making a dictionary
    # keywords_llm = {}
    # for prediction in predictions:
    #     if 'token_str' in prediction and 'score' in prediction:
    #         keywords_llm[prediction['token_str']] = prediction['score']

    keywords_llm = {}
    for predictions in predictions_list:
        for prediction in predictions:
            if 'token_str' in prediction and 'score' in prediction:
                token_str = prediction['token_str']
                score = prediction['score']
                keywords_llm[token_str] = score


    #keywords_llm = {tuple(filtered_words): prediction['score'] for prediction in predictions}


    # Use TF-IDF to extract additional keywords
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(filtered_words)])
    feature_names = vectorizer.get_feature_names_out()

    # Extracting keywords based on TF-IDF and making a dictionary
    tfidf_scores = tfidf_matrix.todense().tolist()[0]
    keywords_tfidf = {feature_names[i]: tfidf_scores[i] for i in range(len(feature_names))}


    # Combine keywords from LLM and TF-IDF
    #all_keywords = {**keywords_llm, **keywords_tfidf}
    all_keywords = {**keywords_tfidf}


    return all_keywords