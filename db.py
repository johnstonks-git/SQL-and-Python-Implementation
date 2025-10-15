import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# Get the path to the database file in the same directory as the app
db_path = Path(__file__).parent / "users.db"

def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, age INTEGER)')
    conn.commit()
    conn.close()
 
def add_user(name, email, age):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO users(name, email, age) VALUES (?,?,?)', (name, email, age))
    conn.commit()
    conn.close()

def view_users():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    data = c.fetchall()
    conn.close()
    return data

def delete_user(user_id):   
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()

create_table()

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.image("https://www.svgrepo.com/show/530438/users.svg", width=100)
choice = st.sidebar.selectbox("Select Action", ["Add User", "View Users", "Delete User"])
st.sidebar.markdown("---")
st.sidebar.info("This app allows you to manage user data in a SQLite database.")

# Main content
st.title("John Gabriel Cruz")

if choice == "Add User":
    st.subheader("Add New User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", 0, 120)

    if st.button("Submit"):
        add_user(name, email, age)
        st.success(f"{name} added successfully")

elif choice == "View Users":
    st.subheader("View All Users")
    users = view_users()
    df = pd.DataFrame(users, columns=["ID", "Name", "Email", "Age"])
    st.dataframe(df)

elif choice == "Delete User":
    st.subheader("Delete a User")
    users = view_users()
    df = pd.DataFrame(users, columns=["ID", "Name", "Email", "Age"])
    st.dataframe(df)
    user_id = st.number_input("Enter ID to delete", 1)
    if st.button("Delete"):
        delete_user(int(user_id))
        st.warning(f"User {user_id} deleted!")