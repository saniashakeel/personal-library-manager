import streamlit as st
import pandas as pd
import json
import datetime
import time
import requests
import os
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie

# SET PAGE CONFIGURATION:
st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Initialize session state variables
if 'library' not in st.session_state:
    st.session_state.library = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

def load_library():
    if os.path.exists('library.json'):
        with open('library.json', 'r') as file:
            st.session_state.library = json.load(file)

def save_library():
    with open('library.json', 'w') as file:
        json.dump(st.session_state.library, file)

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
    st.success("Book added successfully!")

def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        st.success("Book removed successfully!")

# Load Library\load_library()

# Sidebar Navigation
st.sidebar.header("Navigation")
nav_option = st.sidebar.radio("Choose an option:", ["View Library", "Add Book", "Library Statistics"])

if nav_option == "View Library":
    st.session_state.current_view = "library"
elif nav_option == "Add Book":
    st.session_state.current_view = "add"
elif nav_option == "Library Statistics":
    st.session_state.current_view = "stats"

st.title("📚 Personal Library Manager")

if st.session_state.current_view == "add":
    st.subheader("Add a New Book")
    
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.datetime.now().year, step=1)
        with col2:
            genre = st.selectbox("Genre", ["Self-Help", "Art", "Fiction", "Fantasy", "Poetry", "Non-Fiction", "Science", "Technology", "Romance", "History", "Others"])
            read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True) == "Read"
        
        submitted = st.form_submit_button("Add Book")
        if submitted and title and author:
            add_book(title, author, publication_year, genre, read_status)

elif st.session_state.current_view == "library":
    st.subheader("Your Library")
    
    if not st.session_state.library:
        st.warning("Your library is empty. Add some books to get started!")
    else:
        for i, book in enumerate(st.session_state.library):
            with st.expander(f"📖 {book['title']} by {book['author']}"):
                st.write(f"**Publication Year:** {book['publication_year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Status:** {'✅ Read' if book['read_status'] else '📖 Unread'}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Remove", key=f"remove_{i}"):
                        remove_book(i)
                with col2:
                    new_status = not book['read_status']
                    if st.button("Toggle Read Status", key=f"status_{i}"):
                        st.session_state.library[i]['read_status'] = new_status
                        save_library()

elif st.session_state.current_view == "stats":
    st.subheader("Library Statistics")
    
    if not st.session_state.library:
        st.warning("Your library is empty. Add some books to see stats!")
    else:
        total_books = len(st.session_state.library)
        read_books = sum(1 for book in st.session_state.library if book['read_status'])
        unread_books = total_books - read_books
        read_percent = (read_books / total_books) * 100 if total_books > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Books", total_books)
        col2.metric("Read Books", read_books)
        col3.metric("Unread Books", unread_books)
        
        fig = go.Figure(data=[go.Pie(labels=["Read", "Unread"], values=[read_books, unread_books], hole=0.4)])
        fig.update_layout(title_text="Read vs Unread Books")
        st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.write("© 2025 Sania Shakeel - Personal Library Manager")
