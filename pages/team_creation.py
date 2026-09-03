import streamlit as st

from services import io
from models import team_models

st.set_page_config(
    page_title="GTPR - Team creation"
)

st.title("Create a new team:")

with st.form("team_form"):
    team_name = st.text_input("Team name")

    submitted = st.form_submit_button("Create team")

    if submitted:
        team = team_models.Team(name=team_name)
        io.write_team(team)

        st.success("Team created")
        st.switch_page("pages/home_screen.py")

if st.button("Cancel"):
    st.switch_page("pages/home_screen.py")
