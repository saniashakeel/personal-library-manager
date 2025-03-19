import streamlit as st
import pandas as pd
import json
import datetime
import time
import random
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import os

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
if 'search_result' not in st.session_state:
    st.session_state.search_result = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

def load_library():
    try:
        if os.path.exists('library.json'):
            with open('library.json', 'r') as file:
                st.session_state.library = json.load(file)
                return True
        return False
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return False

def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file)
            return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
        return False

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
    time.sleep(0.5)  # Animation delay

def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False

def search_books(search_term, search_by):
    search_term = search_term.lower()
    results = []

    for book in st.session_state.library:
        if search_by == "Title" and search_term in book['title'].lower():
            results.append(book)
        elif search_by == "Author" and search_term in book['author'].lower():
            results.append(book)
        elif search_by == "Genre" and search_term in book['genre'].lower():
            results.append(book)
    
    st.session_state.search_result = results

def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read_status'])
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0

    genres = {}
    authors = {}
    decades = {}

    for book in st.session_state.library:
        # Count genres
        if book['genre'] in genres:
            genres[book['genre']] += 1
        else:
            genres[book['genre']] = 1
        
        # Count authors
        if book['author'] in authors:
            authors[book['author']] += 1
        else:
            authors[book['author']] = 1

        # Count decades
        decade = (book['publication_year'] // 10) * 10
        if decade in decades:
            decades[decade] += 1
        else:
            decades[decade] = 1  

    # Sort data
    genres = dict(sorted(genres.items(), key=lambda x: x[1], reverse=True))
    authors = dict(sorted(authors.items(), key=lambda x: x[1], reverse=True))
    decades = dict(sorted(decades.items(), key=lambda x: x[0]))

    return {
        'total_books': total_books,
        'read_books': read_books,
        'percent_read': percent_read,
        'genres': genres,
        'authors': authors,
        'decades': decades
    }

def create_visulations(stats):
    if stats['total_books'] >0:
        fig_read-status = go.figure(data=[go.Pie(
        labels=['Read','Unread'],
        values=[stats['read_books'],stats['total_books'] - stats['read_books']],
        hole-4,
        marker_colors=['#10B981', '#F87171']
        )])
        fig_read_status.update_layout(
            title_index="Read vs Unread Books",
            showlegend=True,
            height-400
        )
        st.plotly_chart(fig_read_status,use_container_width=True)
        
        #Bar Chart Genres
        if stats['genres']:
            genres_df = pd.DataFrame({
                'Genre':list(stats['genres'].keys()),
                'Count':list(stats['genres'].values())
            })
        fig_genres = px.bar(    
            genres_df,
            x='Genres',
            y='Count',
            color='Count',
            color _continuous_scale=px.colors.sequential.Blues
        )
    fig_genres.update_layout(
        title_text = 'Book by publication genres',
        xaxis_title = 'DGenes',
        yaxis_title= 'Number of books',
        height-400
    )
    st.plotly_chart(fig_genres, use_container_width=True)
if stats['decades'] :
    decades_df = pd.Dataframe({
        'Decade':[f"{decade}s" for decade in stats['decades'].key()],
        'Count':list(stats['decades'].values())
    }) 
    fig_decades = px.line(
        decades_df,
        x='Decade',
        y='Count',
        markers= True,
        line_sape="spline"
    )  
    fig_decades.update_layout(
          title_text = 'Book by publication decades',
        xaxis_title = 'Decades',
        yaxis_title= 'Number of books',
        height-400
    )
     st.plotly_chart(fig_decades, use_container_width=True)

     #Load Library

     load_library()
     st.sidebar.markdown("<h1 style 'text-align: center;'> Navigation</h1>", unsafe_allow_html=True)
     lottie_book = load-lottieurl("https://assests9.lottiefiles.com/temp/1f20_aKAfIn.json")
     if lottie_book:
        with st.sidebar:
            st_lottie(lottie_book, height-200, key-'book_animation')

    nav_option = st.sidebar.radio(
        "Choose an option:",
        ["View Library", "Add Books", "Library Statistics"])        


    if nav_options == "View Library":
        st.session_state.current_view = "library" 
    elif nav_options == "Add Book":
        st.session_state.current_view = "add"
    elif nav_options == "Search Books":
        st.session_state.current_view = "search"
    elif nav_options == "Library Statistics":
        st.session_state.current_view = "stats" 

st.markdown ("<h1 class = 'main-header'> Personal library Manager</h1>", unsafe_allow _html=True)
if st.session_state.current_view == "add":
    st.markdown ("<h2 class = 'sub-header'>Add a new Book/h2>", unsafe_allow_html=True)

   #Adding books input form
   with st.form(key= 'add_book_form'):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Book Title", max_chars=100)
        author = st.text_input("Author", max_chars=100)
        publication_year = st.text_input("Publication Year", min value=1000, max_value=datatime.noe().year, step=1, value=2023)

        with col2:
            genre = st.selectbox("Genre",[
               "Self-Help","Art", "Friction","Fantasy","Poetry", "Non-Friction", "Science", "Technology", "Romance", "Religion", "Novels", "History", "Others"
            ])                          
            
read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
read_bool = read_status =="Read"
submit_button = st.form_submit_button(label="Add Book")

if submit_button and title and author:
    add_book(title , author, publication year, genre, read_bool)

id st.session_state.book_added:
st.markdown ("<div class='success-message'>Book added Successfully!</div>",unsafe_allow_html=True)
st.balloons()
st.session_state.book_added= False
elif st.session_state.current_view =="library":
     st.markdown("<h2 class='sub-header'> Your library )</h2>", unsafe_allow_html=True)

     if not st.session_state.library:
        st.markdown("<div class = 'warning-message'> Your library is empty.Add some books to get started)</div>", unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for i  , book in enumerate(st.session_state.library):
            with cols[ i % 2]:
                st.markdown(f"""<div class = 'book-card'>
                            <h3>{book['title']}</h3>
                            <p><strong>Author:</strong>{book['author']}</p>
                            <p><strong>Publication_year:</strong>{book['publication_year']}</p>
                            <p><strong>Genre:</strong>{book['genre']}</p>
                            <p><span class='{"read-badge"if book["read_status"] else "unread-badge"}'>{
                                "Read" if book["read_status"] else "Unread"           
                            }</span></p>
                            </div>
         """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Remove", key=f"remove_{i}", use_container_width=True):
                        if remove-book(i)
                        st.return()
                    with col2:
                        new_status =not book['read_status']
                        status_label ="Mark as read" if not book['read_status'] else "Mark as read"
                        if st.button(status_label, key=f"status_{i}," use_container width=True)       
                            st.session_state.library[i]['read_status'] = new_status
                            save_library()
                            st.return()
        if st.session_state.book_removed:
            st.markdown("<div class= 'success-message'>Book removed Successfully!</div", unsafe_allow_html=True)
            st.session_state.book_removed = False
        elif st.session_state.book_removed == "search":
            st.markdown("<h2 class ='sub-header'>Search Books</h2>",unsafe_allow-html=True)

            search_by = st.selectbox("Search by:", ["Title","Author","Genre"])
            search_term = st.text_input("Enter search term:")

        if st.button("Search",use_container_width=False):
            if search_term:
                with st.spinner("Searching..."):
                    time.sleep(0.5)
                    search_books(search_term, search_by)
            if hasattr(st.session_state, 'search_results'):
                if st.session_state.search.results:
                    st.markdown(f"<h3>Found{len(st.session_state.search_results)}results:</h3>", unsafe_allow_html=True)
                           
            for i, book in enumerates(s.session_state.search_results):
            <h3>{book['title']}</h3>
            st.markdown(f""" 
                                    <p><strong>Author:</strong>{book['author']}</p>
                            <p><strong>Publication_year:</strong>{book['publication_year']}</p>
                            <p><strong>Genre:</strong>{book['genre']}</p>
                            <p><span class='{"read-badge"if book["read_status"] else "unread-badge"}'>{
                                "Read" if book["read_status"] else "Unread"           
                            }</span></p>
                            </div>   
            """,unsafe_allow_html=True)
    elif search_term:
                    st.markdown("<div class= 'warning-message'> No books found matching of your search.</div>")

    elif st.session_state.current_view == "stats":
        st.markdown("<h2 class ='sub-header'>Library Statistics</h2>", unsafe_allow_html=True)
 
    if not st.session_state.library:
        st.markdown("<div class= 'warning-message'>Your library is empty.Add some books to see stats!</div>", unsafe_allow_html=True)
    else:
        stats = get_library_stats()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", stats['total books'])
        with col2:
            st.metric("Read Books", stats['read books'])
        with col3:
            st.metric("Percentage Read", f"{stats['percentage read'] :.if}%")
        create_visulations()                
                  
        if stats['authors']:
            st.markdown("<h3> Top Authors</h3>", unsafe_allow_html=True)
            top_authors = dict(list(stats['author'].item())[:5])
            for author , count in top_authors.item():
                st.markdown(f"**{author}**: {count} book{'s' if count > 1 else ''}")
st.markdown("---")
st.markdown("Copyright @ 2025 Sania Shakeel Personal Library Manager", unsafe_allow_html=True)
