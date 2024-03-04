import streamlit as st
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def stream_data(stream):
    for r in stream:
        yield r.raw['content']['parts'][0]['text'] + ""


@st.cache
def load_embed_model():
    return HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )