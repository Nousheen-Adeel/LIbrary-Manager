import streamlit as st
import json
import os

FILE = 'library.txt'

def load_data():
    if os.path.exists(FILE):
        with open(FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE, 'w') as f:
        json.dump(data, f)

def add_book(library, title, author, year, genre, read):
    library.append({
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read
    })
    save_data(library)

def remove_book(library, title):
    updated = [book for book in library if book['title'].lower() != title.lower()]
    save_data(updated)
    return updated

# UI
st.title("📚 Library Manager")

library = load_data()
menu = st.sidebar.selectbox("Menu", ["Add Book", "Remove Book", "Search", "View All", "Statistics"])

if menu == "Add Book":
    with st.form("add_book"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.text_input("Year")
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read it?")
        if st.form_submit_button("Add"):
            add_book(library, title, author, year, genre, read)
            st.success(f"'{title}' added!")

elif menu == "Remove Book":
    title = st.text_input("Enter title to remove")
    if st.button("Remove"):
        library = remove_book(library, title)
        st.success(f"'{title}' removed (if it existed).")

elif menu == "Search":
    by = st.radio("Search by", ["title", "author"])
    term = st.text_input(f"Enter {by}")
    if term:
        results = [b for b in library if term.lower() in b[by].lower()]
        for b in results:
            st.write(f"**{b['title']}** by {b['author']} ({b['year']}) - {b['genre']} - {'✅ Read' if b['read'] else '❌ Unread'}")
        if not results:
            st.warning("No results found.")

elif menu == "View All":
    if library:
        for b in library:
            st.write(f"**{b['title']}** by {b['author']} ({b['year']}) - {b['genre']} - {'✅ Read' if b['read'] else '❌ Unread'}")
    else:
        st.info("Library is empty.")

elif menu == "Statistics":
    total = len(library)
    read = sum(1 for b in library if b['read'])
    percent = (read / total) * 100 if total else 0
    st.metric("Total Books", total)
    st.metric("Books Read", read)
    st.metric("Read Percentage", f"{percent:.2f}%")
