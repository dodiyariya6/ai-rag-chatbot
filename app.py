import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

st.set_page_config(page_title="AI RAG Chatbot")
st.title("🤖 AI RAG Chatbot")


@st.cache_resource
def load_embedding():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


@st.cache_resource
def load_db():
    embedding = load_embedding()
    return Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding
    )


@st.cache_resource
def load_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash"
    )


db = load_db()
llm = load_llm()

question = st.text_input("Ask a question:")

if question:

    with st.spinner("🤖 Thinking..."):

        docs = db.similarity_search(question, k=2)

        context = "\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
        Answer using only the context below.

        Context:
        {context}

        Question:
        {question}
        """

        response = llm.invoke(prompt)

        st.subheader("Answer")
        st.write(response.content)