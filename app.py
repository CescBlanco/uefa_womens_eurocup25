import pandas as pd
import numpy as np
from datetime import datetime
from statsbombpy import sb
import streamlit as st

from mplsoccer import VerticalPitch, Pitch
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.colors import to_rgba
import seaborn as sns

from functions.functions import *
from visualizations.visualizations import *

pd.options.display.max_columns = None


# Título de la app
st.set_page_config(page_title="⚽ UEFA - WOMEN'S EUROCUP 2025", layout="wide")

col1, col2, col3= st.columns([1, 3, 1])

with col1: 
    logo_eurocup = mpimg.imread('./assets/UEFA_Women_s_Euro_2025_logo.svg-removebg-preview.png') 
    
    st.image(logo_eurocup, width=150)

with col2:
    st.markdown("""
    <h1 style='text-align: center; color: #2E86C1; margin-bottom: 0.1em;'>
        ⚽ UEFA - WOMEN'S EUROCUP 2025
    </h1>
    """, unsafe_allow_html=True)

with col3: 
    logo_eurocup = mpimg.imread('./assets/logo_statsbomb.png') 
    
    st.image(logo_eurocup, width=300)


free_comps = sb.competitions()
eurocupfem_2025 = sb.matches(53, 315).sort_values(by='match_date').reset_index(drop= True)
eurocupfem_2025= convert_match_date(eurocupfem_2025)
eurocupfem_2025_final= extract_interest_columns(eurocupfem_2025)

# Listas iniciales (todas las opciones)
stages_list, teams_list, dates_list = get_dynamic_lists(eurocupfem_2025_final)

# Columnas en streamlit
col1, col2, col3 = st.columns(3)

with col1:
    round_selected = st.selectbox("🔁 Select the round:", stages_list)

# Actualizar listas en base a lo elegido en col1
stages_list, teams_list, dates_list = get_dynamic_lists(
    eurocupfem_2025_final,
    round_select=round_selected
)

with col2:
    team_selected = st.selectbox("👕 Select the team:", teams_list)

# Actualizar listas en base a lo elegido en col1 + col2
stages_list, teams_list, dates_list = get_dynamic_lists(
    eurocupfem_2025_final,
    round_select=round_selected,
    team_select=team_selected
)

with col3:
    match_date_selected = st.selectbox("📆 Select the date match:", dates_list)

st.markdown(
        f"<h3 style='margin-top: 1em; color: #999; text-align:center; font-weight:bold;'> 📝 Matches details post filter</h3>",
                        unsafe_allow_html=True)
st.write('')
matches_from_filter, definition_info_matches_filter = dataframe_extraction(
    eurocupfem_2025_final,
    date_select=match_date_selected,
    team_select=team_selected,
    round_select=round_selected
)

matches_from_filter_with_logos = add_team_logos(matches_from_filter)

# Número de columnas que queremos por fila
num_cols = 2

# Iteramos por parejas de partidos
for i in range(0, len(matches_from_filter_with_logos), num_cols):
    row_matches = matches_from_filter_with_logos.iloc[i:i+num_cols]
    cols = st.columns(num_cols)
    
    for col, (_, row) in zip(cols, row_matches.iterrows()):
        home_logo_b64 = img_to_base64(row['home_logo_path'])
        away_logo_b64 = img_to_base64(row['away_logo_path'])
        
        with col:
            st.markdown(
                f"""
                <div style="border:1px solid #ddd; border-radius:10px; padding:10px; margin:10px 0; text-align:center;">
                    <h4>{row['match_date_convert']} | {row['kick_off']}</h4>
                    <div style="display:flex; justify-content:center; align-items:center; gap:20px;">
                        <div>
                            <img src="data:image/png;base64,{home_logo_b64}" width="60"><br>
                            <b>{row['home_team']}</b>
                        </div>
                        <div style="font-size:24px; font-weight:bold;">
                            {row['home_score']} - {row['away_score']}
                        </div>
                        <div>
                            <img src="data:image/png;base64,{away_logo_b64}" width="60"><br>
                            <b>{row['away_team']}</b>
                        </div>
                    </div>
                    <p><i>{row['competition_stage']} | {row['stadium']}</i></p>
                    <p><b>Referee:</b> {row['referee']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Gestión de selección de partido ---
if round_selected.lower() == "all":
    st.warning("⚠️ Cannot access detailed visualizations when 'All' rounds are selected.")
else:
    if len(matches_from_filter_with_logos) > 1:
        # Crear lista de partidos para selección
        match_options = [
            f"{row['home_team']} vs {row['away_team']} ({row['match_date_convert']} | {row['kick_off']})"
            for _, row in matches_from_filter_with_logos.iterrows()
        ]
        selected_match_str = st.selectbox("Select a match to visualize", match_options)
        selected_index = match_options.index(selected_match_str)
        selected_match = matches_from_filter_with_logos.iloc[selected_index]
        
        match_id_selected_more_options = selected_match['match_id']  # <-- Aquí ya tienes el match_id para tus visualizaciones
        match_id = match_id_selected_more_options

        # Filtrar solo el partido seleccionado
        selected_match_df = matches_from_filter_with_logos[matches_from_filter_with_logos['match_id'] == match_id]
        
    else:
        # Solo hay un partido filtrado
        match_id_selected_one_match= matches_from_filter_with_logos.iloc[0]['match_id']
        match_id = match_id_selected_one_match

        # Filtrar solo el partido seleccionado
        selected_match_df = matches_from_filter_with_logos[matches_from_filter_with_logos['match_id'] == match_id]
        st.dataframe(selected_match_df)


    st.write(match_id)
    match_events= sb.events((match_id))

    df_home_lineup, formation_home, df_away_lineup, formation_away= search_lineups_match(match_events, DICTIONARY_NAMES) 
    dataframe_formations_mplsoccer= create_df_formations()
    home_formation_df, away_formation_df= extractions_df_formations(dataframe_formations_mplsoccer, formation_home, formation_away)


    # Crear pestañas
        
    titles_tabs = [
            "📊📑 MATCH STADISTICS",
            "📈⚽️ MATCH VISUALITZACIONS"
        ]

    tabs = st.tabs(titles_tabs)

    with tabs[0]:
            
        select_section = ["LINEUPS", "GENERAL STADISTICS OF DE MATCH", "AVERAGE POSITIONS" ]
        chosen_section = st.radio("Select what you want to see:", select_section, horizontal=True)

        if chosen_section == "LINEUPS":
            
            colplotlineups1, colplotlineups2 = st.columns(2)

            with colplotlineups1:
                st.markdown(
                f"<h4 style='margin-top: 1em; color: #999; text-align:center; font-weight:bold;'> STARTING XI HOME</h4>",
                                unsafe_allow_html=True)
                plot_lineups_home= plot_lineups(selected_match_df, formation_home, df_home_lineup , home= True )
                st.pyplot(plot_lineups_home )

                coach_name_home=find_coach_name(selected_match_df, home= True)

                st.markdown(
                f'<p style="text-align: center;"><b>LOCAL COACH: {coach_name_home}</b></p>',
                unsafe_allow_html=True)


            with colplotlineups2:
                st.markdown(
                f"<h4 style='margin-top: 1em; color: #999; text-align:center; font-weight:bold;'> STARTING XI AWAY</h4>",
                                unsafe_allow_html=True)
                plot_lineups_away= plot_lineups(selected_match_df, formation_away, df_away_lineup , home= False )
                st.pyplot(plot_lineups_away)

                coach_name_away=find_coach_name(selected_match_df, home= False)

                st.markdown(
                f'<p style="text-align: center;"><b>AWAY COACH: {coach_name_away}</b></p>',
                unsafe_allow_html=True)

        elif chosen_section == "GENERAL STADISTICS OF DE MATCH":
            st.write('Builing')

        else:
            st.write('Builing') 

    with tabs[1]:
        select_section_plot= ["HEATMAPS", "SHOTMAPS", "NETWORK PASS" ]
        chosen_section_plot = st.radio("Select the plot you want to view:", select_section_plot, horizontal=True)

        if chosen_section_plot == "HEATMAPS":
            st.write('BUILDING')

        elif chosen_section_plot == "SHOTMAPS":

            st.dataframe(selected_match_df)
            st.write(match_id)
            home_name_team, away_name_team=names_home_away_teams(selected_match_df, match_id)
            st.write(home_name_team)
            st.write(away_name_team)
        
        else:
            home_name_team, away_name_team=names_home_away_teams(selected_match_df, match_id)
            pass_event_home, pass_event_away= dataframe_pass_for_teams(match_events,home_name_team, away_name_team, DICTIONARY_NAMES)
            colors_home, colors_away= get_colors_team(home_name_team, away_name_team, TEAM_COLORS_PRIMARY)

            # Filtro de tiempo del partido con selectbox
            time_options = ["All match", "First Half", "Second Half"]
            time_selected = st.selectbox("⏱️ Select period to visualize:", time_options)

            title_map = {
                "All match": "📊 Passing Network - Full Match",
                "First Half": "📊 Passing Network - 1st Half",
                "Second Half": "📊 Passing Network - 2nd Half"
            }
            # Filtrado según selección
            if time_selected == "First Half":
                pass_event_home_1part = pass_event_home[pass_event_home["period"] == 1]


                pass_event_away_1part = pass_event_away[pass_event_away["period"] == 1]
                
                st.markdown(
                    f"<h4 style='text-align:center; font-weight:bold;'>{title_map[time_selected]}</h4>",
                    unsafe_allow_html=True
                )


                col_passnetwork1part1, col_passnetwork1part2 = st.columns(2)

                with col_passnetwork1part1:
                
                    st.markdown(
                        f"<h4 style='margin-top: 1em; color: #999; text-align:center; font-weight:bold;'> HOME</h4>",
                                        unsafe_allow_html=True)

                    pass_between_home, average_locations_home_sub= preparation_plot_networkpass(match_events,pass_event_home_1part,  home_name_team, DICTIONARY_NAMES )
                    plot_networkpass_home_1part= plot_network_pass(pass_between_home, average_locations_home_sub,colors_home )
                    st.pyplot(plot_networkpass_home_1part)

                with col_passnetwork1part2:
                
                    st.markdown(
                        f"<h4 style='margin-top: 1em; color: #999; text-align:center; font-weight:bold;'> AWAY</h4>",
                                        unsafe_allow_html=True)

                    pass_between_away, average_locations_away_sub= preparation_plot_networkpass(match_events,pass_event_away_1part,  away_name_team,DICTIONARY_NAMES)
                    plot_networkpass_away_1part= plot_network_pass(pass_between_away, average_locations_away_sub,colors_away )
                    st.pyplot(plot_networkpass_away_1part)


            elif time_selected == "Second Half":
                pass_event_home_2part = pass_event_home[pass_event_home["period"] == 2]
                
                pass_event_away_2part = pass_event_away[pass_event_away["period"] == 2]
            
                st.markdown(
                    f"<h4 style='text-align:center; font-weight:bold;'>{title_map[time_selected]}</h4>",
                    unsafe_allow_html=True
                )

                col_passnetwork2part1, col_passnetwork2part2 = st.columns(2)

                with col_passnetwork2part1:
                
                    st.markdown(
                        f"<h4 style='margin-top: 1em; color: #999; text-align:center; font-weight:bold;'> HOME</h4>",
                                        unsafe_allow_html=True)

                    pass_between_home, average_locations_home= preparation_plot_networkpass_2half(match_events,pass_event_home_2part,  home_name_team, DICTIONARY_NAMES )
                    plot_networkpass_home_2part= plot_network_pass(pass_between_home, average_locations_home,colors_home )
                    st.pyplot(plot_networkpass_home_2part)

                with col_passnetwork2part2:
                
                    st.markdown(
                        f"<h4 style='margin-top: 1em; color: #999; text-align:center; font-weight:bold;'> AWAY</h4>",
                                        unsafe_allow_html=True)

                    pass_between_away, average_locations_away= preparation_plot_networkpass_2half(match_events,pass_event_away_2part,  away_name_team, DICTIONARY_NAMES)
                    plot_networkpass_away_2part= plot_network_pass(pass_between_away, average_locations_away,colors_away )
                    st.pyplot(plot_networkpass_away_2part)

            else:  # "All match"
            

                st.markdown(
                    f"<h4 style='text-align:center; font-weight:bold;'>{title_map[time_selected]}</h4>",
                    unsafe_allow_html=True
                )
                st.info(
                    "ℹ️ For the **whole match plots**, only passes before the first substitution are considered."
                )

                col_passnetwork1, col_passnetwork2 = st.columns(2)

                with col_passnetwork1:
                
                    st.markdown(
                        f"<h4 style='margin-top: 1em; color: #999; text-align:center; font-weight:bold;'> HOME</h4>",
                                        unsafe_allow_html=True)

                    pass_between_home, average_locations_home_sub= preparation_plot_networkpass(match_events,pass_event_home,  home_name_team, DICTIONARY_NAMES )
                    plot_networkpass_home= plot_network_pass(pass_between_home, average_locations_home_sub,colors_home )
                    st.pyplot(plot_networkpass_home)

                with col_passnetwork2:
                
                    st.markdown(
                        f"<h4 style='margin-top: 1em; color: #999; text-align:center; font-weight:bold;'> AWAY</h4>",
                                        unsafe_allow_html=True)

                    pass_between_away, average_locations_away_sub= preparation_plot_networkpass(match_events,pass_event_away,  away_name_team, DICTIONARY_NAMES )
                    plot_networkpass_away= plot_network_pass(pass_between_away, average_locations_away_sub,colors_away )
                    st.pyplot(plot_networkpass_away)