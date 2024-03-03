# app.py
import streamlit as st
from analyzer import analyze_job_description
import pandas as pd
import numpy as np
from annotated_text import annotated_text
from highlighter import highlight_words_in_text

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

def main():
    st.title("Job Insight")
    job_description = st.text_area("Enter the job description:")
    analyze_button = st.button("Analyze")


    if analyze_button:
        result = {}
        max_chunk_length = 512  # Set the maximum sequence length for the BERT model

        # Split the job description into chunks
        chunks = [job_description[i:i + max_chunk_length] for i in range(0, len(job_description), max_chunk_length)]

        # Process each chunk and accumulate the results
        for chunk in chunks:
            chunk_result = analyze_job_description(chunk)
            result.update(chunk_result)

        # Separate the words and counts into lists
        words = list(result.keys())
        counts = [count.toarray()[0][0] if isinstance(count, np.matrix) else count for count in result.values()]

        # Create a DataFrame from the lists
        df = pd.DataFrame({"Word": words, "Count": counts})
        df['Count'] = df['Count'].fillna(0)

        # Sort the DataFrame based on 'Count' in descending order
        df = df.sort_values(by='Count', ascending=False)

        # Create and display a table
        st.write("Keywords and Counts:")
        st.dataframe(df, use_container_width=True)

        highlighted_text = highlight_words_in_text(job_description, words, background="#FF0", color="black")
        st.markdown(str(highlighted_text), unsafe_allow_html=True)

if __name__ == "__main__":
    main()