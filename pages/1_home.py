import streamlit as st
from services import io

st.title("Genshin Team Power Ranking")

st.metric("Total Teams", len(st.session_state.teams))
st.divider()

if not st.session_state.teams:
    st.info("No teams found. Go to the Team Builder to create one!")

for team in st.session_state.teams:
    with st.expander(f"🛡️ Team: {team.name}"):
        st.write(f"**Characters:** {', '.join([c.name for c in team.character_builds])}")

        if st.button("Delete Team", key=f"del_{team.name}", type="primary"):
            io.delete_team(team.name)
            st.session_state.teams = io.read_teams()
            st.rerun()
