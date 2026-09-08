import streamlit as st
from models.team_models import Team
from services import io

st.set_page_config(layout="wide")

col_select, col_create = st.columns([2, 1])

with col_select:
    if st.session_state.teams:
        team_names = [t.name for t in st.session_state.teams]
        selected_team_name = st.selectbox("Load Team", team_names, label_visibility="collapsed")
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
    col_title.title(f"{active_team.name}")
    if col_save.button("💾 Save Team Changes", use_container_width=True):
        io.write_team(active_team)
        st.success("Saved!")

    st.write("")

    char_cols = st.columns(4)

    for i, col in enumerate(char_cols):
        char = active_team.character_builds[i]

        prefix = f"{active_team.name}_char{i}"

        with col:
            with st.container(border=True):
                char.name = st.text_input(f"Slot {i+1}", value=char.name, label_visibility="collapsed", key=f"{prefix}_name")
                st.divider()

                char.dps_floor = st.number_input("DPS Floor", value=char.dps_floor, step=100, key=f"{prefix}_floor")
                char.dps_ceiling = st.number_input("DPS Ceiling", value=char.dps_ceiling, step=100, key=f"{prefix}_ceil")
                char.roll_value = st.number_input("Roll Value", value=char.roll_value, step=100, key=f"{prefix}_roll")

                st.divider()

                if active_team.team_dps > 0 and char.dps_ceiling > char.dps_floor:
                    progress = char.get_progress(active_team.team_dps)
                    upgrade_difficulty_modifier = char.get_upgrade_difficulty()
                    raw_score = char.get_raw_priority_score(active_team.team_dps)
                    rel_score = active_team.get_relative_priority_score(char)

                    st.metric("Build Progress", f"{progress * 100:.1f}%")
                    st.metric("Artifact upgrade difficulty modifier", f"{upgrade_difficulty_modifier * 100:.2f}%")
                    st.metric("Expected DPS Return", f"{raw_score:,.0f}")
                    st.metric("Team Focus Priority", f"{rel_score * 100:.1f}%")
                else:
                    st.metric("Build Progress", "0.0%")
                    st.metric("Expected DPS Return", "0")
                    st.metric("Team Focus Priority", "0.0%")

    st.write("")

    st.subheader("Total Team Performance")
    with st.container(border=True):
        bot_col1, bot_col2, bot_col3 = st.columns([1.5, 1.5, 3])

        with bot_col1:
            st.metric("Current Team Output", f"{active_team.team_dps:,} DPS")

        with bot_col2:
            active_team.team_dps = st.number_input(
                "Edit Team DPS",
                value=active_team.team_dps,
                step=500,
                key=f"{active_team.name}_team_dps"
            )

        with bot_col3:
            st.info("Modifying any input field instantly updates all progress and priority metrics above.")
