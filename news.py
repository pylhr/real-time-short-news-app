import streamlit as st
import json
import requests
from newspaper import Article
from transformers import pipeline

# Set Streamlit page configuration
st.set_page_config(
    page_title="Short News App", layout="wide", initial_sidebar_state="expanded"
)

# Page title
st.title(
    "Welcome to Short News App\n"
    "Tired of reading long articles? This app summarizes news articles for you and gives you short, crispy, to-the-point news based on your search.\n"
    "(This is a demo app and hence is deployed on a platform with limited computational resources. The number of articles this app can fetch is limited to 5)"
)

# Summarization pipeline
summarizer = pipeline("summarization")

# Containers for article information
article_titles = []
article_texts = []
article_summaries = []
article_urls = []


def run():
    with st.sidebar.form(key="form1"):
        search = st.text_input("Search your favorite topic:")
        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                url = "https://newsapi.org/v2/everything"
                querystring = {
                    "q": search,
                    "apiKey": "ac5a0256a2fc442096b908d50ac2926c",
                    "language": "en",
                    "sortBy": "relevancy",
                    "domains": "thehindu.com,indiatimes.com,ndtv.com,indianexpress.com,hindustantimes.com",
                }

                response = requests.get(url, params=querystring)
                response_dict = response.json()

                if response_dict["status"] == "ok":
                    articles = response_dict["articles"][:5]

                    for article in articles:
                        article_titles.append(article["title"])
                        article_urls.append(article["url"])

                        news_article = Article(article["url"])
                        news_article.download()
                        news_article.parse()
                        article_texts.append(news_article.text)

                    for text in article_texts:
                        if text:
                            summary = summarizer(
                                text, max_length=150, min_length=25, do_sample=False
                            )[0]["summary_text"]
                            article_summaries.append(summary)
                        else:
                            article_summaries.append(
                                "No content available to summarize."
                            )
                else:
                    st.error("Error fetching articles. Please try again later.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

    for i in range(len(article_texts)):
        st.header(article_titles[i])
        st.subheader("Summary of Article")
        st.markdown(article_summaries[i])
        with st.expander("Full Article"):
            st.markdown(article_texts[i])
            st.markdown(f"[Read more at the source]({article_urls[i]})")


if __name__ == "__main__":
    run()
