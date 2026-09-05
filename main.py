import streamlit as st
from services import io

st.set_page_config(page_title="GTPR", layout="wide")

if "teams" not in st.session_state:
    st.session_state.teams = io.read_teams()

pages = {
    "Teams": [
        st.Page("pages/1_home.py", title="Dashboard"),
        st.Page("pages/2_team_builder.py", title="Team Builder"),
    ],
}

pg = st.navigation(pages)
pg.run()