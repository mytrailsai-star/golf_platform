import streamlit as st
import requests

API = "http://127.0.0.1:5000"

st.title("🏌️ Golf Charity Platform")

menu = st.sidebar.selectbox("Menu", ["Signup", "Login", "Dashboard"])

# -------- SIGNUP --------
if menu == "Signup":
    st.subheader("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        res = requests.post(f"{API}/signup", json={
            "email": email,
            "password": password
        })
        st.success("Account created!")

# -------- LOGIN --------
elif menu == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API}/login", json={
            "email": email,
            "password": password
        })

        if res.status_code == 200:
            st.session_state.user_id = res.json()["user_id"]
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# -------- DASHBOARD --------
elif menu == "Dashboard":
    if "user_id" not in st.session_state:
        st.warning("Please login first")
    else:
        user_id = st.session_state.user_id

        st.subheader("Subscription")
        if st.button("Subscribe"):
            requests.post(f"{API}/subscribe", json={"user_id": user_id})
            st.success("Subscribed!")

        st.subheader("Add Score")
        score = st.number_input("Score (1-45)", min_value=1, max_value=45)

        if st.button("Submit Score"):
            requests.post(f"{API}/add_score", json={
                "user_id": user_id,
                "score": score
            })
            st.success("Score added!")

        st.subheader("Your Scores")
        scores = requests.get(f"{API}/scores/{user_id}").json()
        st.write(scores)

        st.subheader("Draw")
        if st.button("Run Draw"):
            draw = requests.get(f"{API}/draw").json()
            st.success(f"Draw Numbers: {draw}")