import streamlit as st
import requests
from datetime import datetime
from gtts import gTTS #"this is used for text to speech"
import os
import tempfile
import re

# Page Config
st.set_page_config(page_title="📰 NewsNow - Your Personal Headline Hub", layout="wide")
st.title("📰 NewsNow")
st.subheader("Fetch the latest headlines by category, keyword, and more.")

category = st.selectbox(
    "Select a news category:",
    ["business", "entertainment", "general", "health", "science", "sports", "technology"]
)


keyword = st.text_input("Enter keyword to search in headlines (optional):", "")


sort_order = st.radio("Sort articles by:", ["Newest First", "Oldest First"])

api_key = "" # Your API Key from https://www.newsapi.ai
url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&q={keyword}&apiKey={api_key}"

if st.button("🔍 Get News"):
    response = requests.get(url)

    if response.status_code == 200:
        news = response.json()
        articles = news.get("articles", [])

        if not articles:
            st.warning("No articles found for the given criteria.")
        else:
            # Sort articles
            articles = sorted(
                articles,
                key=lambda x: x["publishedAt"] or "",
                reverse=(sort_order == "Newest First")
            )

            st.success(f"Showing {len(articles)} articles in '{category}' category")

            for idx, article in enumerate(articles):
                with st.container():
                    st.markdown(f"### {article['title']}")

                    if article.get("urlToImage"):
                        st.image(article["urlToImage"], width=600)

                    description = article.get("description", "")

                    content = article.get("content", "")
                    cleaned_content = re.sub(r'<[^>]*>', '', content or "")
                    cleaned_content = re.sub(r'\[\+\d+\s+chars\]', '', cleaned_content)

                    full_text = f"{description}\n\n{cleaned_content}".strip()

                    max_chars = 1500
                    display_text = full_text
                    if len(display_text) > max_chars:
                        display_text = display_text[:max_chars].rsplit(" ", 1)[0] + "..."

                    st.write(display_text or "*No detailed content available.*")

                    if full_text.strip():
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            tts = gTTS(text=full_text, lang='en')
                            tts.save(fp.name)
                            st.audio(fp.name, format="audio/mp3", start_time=0)
                    else:
                        st.info("🔈 No voice summary available for this article.")

                    pub_time = article["publishedAt"]
                    if pub_time:
                        pub_time = datetime.strptime(pub_time, '%Y-%m-%dT%H:%M:%SZ')
                        pub_time = pub_time.strftime('%b %d, %Y %I:%M %p')

                    st.caption(f"Published at: {pub_time} | Source: {article['source']['name']}")
                    st.markdown(f"[📖 Read Full Article]({article['url']})")
                    st.markdown("---")
    else:
        st.error(f"Failed to fetch news. Status Code: {response.status_code}")
