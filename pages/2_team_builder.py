import streamlit as st
from models.team_models import Team
from services import io

st.set_page_config(layout="wide")

col_select, col_create = st.columns([2, 1])

with col_select:
    if st.session_state.teams:
        team_names = [t.name for t in st.session_state.teams]
        selected_team_name = st.selectbox("Load Team Dashboard", team_names, label_visibility="collapsed")
        active_team = next(t for t in st.session_state.teams if t.name == selected_team_name)
    else:
        st.warning("No teams found. Create one below.")
        active_team = None

with col_create:
    with st.popover("Create New Team"):
        new_team_name = st.text_input("New Team Name")
        if st.button("Create"):
            if new_team_name:
                new_team = Team(name=new_team_name)
                st.session_state.teams.append(new_team)
                io.write_team(new_team)
                st.rerun()

st.divider()

if active_team:
    col_title, col_save = st.columns([5, 1])
    col_title.title(f"📊 {active_team.name} Dashboard")
    if col_save.button("💾 Save Dashboard Changes", use_container_width=True):
        io.write_team(active_team)
        st.success("Saved!")

    st.write("")

    char_cols = st.columns(4)

    for i, col in enumerate(char_cols):
        char = active_team.character_builds[i]
        with col:
            with st.container(border=True):
                char.name = st.text_input(f"Slot {i+1}", value=char.name, label_visibility="collapsed", key=f"name_{i}")
                st.divider()

                char.dps_floor = st.number_input("DPS Floor", value=char.dps_floor, step=100, key=f"floor_{i}")
                char.dps_ceiling = st.number_input("DPS Ceiling", value=char.dps_ceiling, step=100, key=f"ceil_{i}")
                char.roll_value = st.number_input("Roll Value", value=char.roll_value, step=100, key=f"roll_{i}")

                st.divider()

                if active_team.team_dps > 0 and char.dps_ceiling > char.dps_floor:
                    progress = char.get_progress(active_team.team_dps)
                    difficulty = char.get_upgrade_difficulty()
                    score = char.get_priority_score(active_team.team_dps)

                    st.metric("Build Progress", f"{progress * 100:.1f}%")
                    st.metric("Upgrade difficulty modifier", f"{difficulty:.3f}")
                    st.metric("Priority Score", f"{score:.3f}")
                else:
                    st.metric("Build Progress", "0.0%")
                    st.metric("Priority Score", "0.000")

    st.write("")

    st.subheader("Total Team Performance")
    with st.container(border=True):
        bot_col1, bot_col2 = st.columns([1, 3])

        with bot_col1:
            active_team.team_dps = st.number_input(
                "Overall Team DPS",
                value=active_team.team_dps,
                step=500
            )

        with bot_col2:
            st.info("Update the overall Team DPS to instantly recalculate Character Progress and Priority Scores across all columns.")
