import streamlit as st
import pandas as pd
import json
import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
import requests
import os

# Set Page Configuration
st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Library Data
def load_library():
    if os.path.exists('library.json'):
        with open('library.json', 'r', encoding="utf-8") as file:
            try:
                st.session_state.library = json.load(file)
            except json.JSONDecodeError:
                st.session_state.library = []
    else:
        st.session_state.library = []

def save_library():
    with open('library.json', 'w', encoding="utf-8") as file:
        json.dump(st.session_state.library, file, indent=4, ensure_ascii=False)

# Load library on startup
if "library" not in st.session_state:
    load_library()

# Initialize session state variables
if 'search_result' not in st.session_state:
    st.session_state.search_result = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

# Add Book Function
def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': publication_year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)
    st.experimental_rerun()

# Remove Book Function
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        st.experimental_rerun()

# Search Books Function
def search_books(search_term, search_by):
    if search_term.strip():  # Prevent empty searches
        search_term = search_term.lower()
        st.session_state.search_result = [
            book for book in st.session_state.library if search_term in book[search_by].lower()
        ]
    else:
        st.session_state.search_result = []

# Sidebar Navigation
st.sidebar.markdown("<h1 style='text-align: center;'>📚 Navigation</h1>", unsafe_allow_html=True)
nav_option = st.sidebar.radio(
    "Choose an option:",
    ["View Library", "Add Book", "Search Books", "Library Statistics"]
)

# Update current view
st.session_state.current_view = {
    "View Library": "library",
    "Add Book": "add",
    "Search Books": "search",
    "Library Statistics": "stats"
}[nav_option]

# Main Header
st.markdown("<h1 class='main-header'>📖 Personal Library Manager</h1>", unsafe_allow_html=True)

# 📌 View Library
if st.session_state.current_view == "library":
    st.markdown("<h2 class='sub-header'>📚 Your Library</h2>", unsafe_allow_html=True)

    if not st.session_state.library:
        st.warning("Your library is empty. Add some books to get started!")
    else:
        for i, book in enumerate(st.session_state.library):
            with st.expander(f"📖 {book['title']}"):
                st.write(f"**Author:** {book['author']}")
                st.write(f"**Publication Year:** {book['publication_year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Status:** {'✅ Read' if book['read_status'] else '📌 Unread'}")

                if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                    remove_book(i)

# 📌 Add Book
if st.session_state.current_view == "add":
    st.markdown("<h2 class='sub-header'>➕ Add a New Book</h2>", unsafe_allow_html=True)
    
    with st.form(key='add_book_form'):
        title = st.text_input("📖 Book Title")
        author = st.text_input("✍️ Author")
        publication_year = st.number_input("📅 Publication Year", min_value=1000, max_value=datetime.datetime.now().year, step=1, value=2023)
        genre = st.selectbox("🎭 Genre", ["Fiction", "Non-Fiction", "Science", "Fantasy", "Biography", "History", "Other"])
        read_status = st.radio("📚 Read Status", ["Read", "Unread"])
        submit_button = st.form_submit_button("✅ Add Book")

        if submit_button:
            if title.strip() and author.strip():  # Ensure input fields are not empty
                add_book(title, author, publication_year, genre, read_status == "Read")
                st.success("Book added successfully!")
            else:
                st.error("❌ Please fill in all fields.")

# 📌 Search Books
if st.session_state.current_view == "search":
    st.markdown("<h2 class='sub-header'>🔍 Search Books</h2>", unsafe_allow_html=True)
    
    search_by = st.selectbox("🔎 Search by:", ["title", "author", "genre"])
    search_term = st.text_input("🔍 Enter search term:")
    
    if st.button("🔍 Search"):
        search_books(search_term, search_by)

    if st.session_state.search_result:
        for book in st.session_state.search_result:
            with st.expander(f"📖 {book['title']}"):
                st.write(f"**Author:** {book['author']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Status:** {'✅ Read' if book['read_status'] else '📌 Unread'}")
    elif search_term:
        st.warning("🚫 No books found matching your search.")

st.markdown("---")
st.markdown("<p style='text-align:center;'>📌 Copyright © 2025 Sania Shakeel | Personal Library Manager</p>", unsafe_allow_html=True)
