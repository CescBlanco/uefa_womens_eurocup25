import pandas as pd
import numpy as np
from datetime import datetime
from statsbombpy import sb
import streamlit as st

from mplsoccer import VerticalPitch, Pitch
import matplotlib.pyplot as plt 
import seaborn as sns

import os
import base64

def convert_match_date(df):
    # 1. Convertir columna original a datetime
    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")
    
    # 2. Crear nueva columna en formato día-mes-año
    df["match_date_convert"] = df["match_date"].dt.strftime("%d-%m-%Y")

    df["kick_off"] = pd.to_datetime(df["kick_off"], errors="coerce").dt.strftime("%H:%M")
    
    return df

def extract_interest_columns(df):
    columnas_interest = ['match_id', 'match_date_convert', 'kick_off', 'home_team', 'away_team', 'home_score', 'away_score',
                     'competition_stage', 'stadium', 'referee', 'home_managers', 'away_managers' ]
    eurocupfem_2025_final = df[columnas_interest].sort_values(by=['match_date_convert', 'kick_off']).reset_index(drop=True)
    return eurocupfem_2025_final

def get_dynamic_lists(df, round_select="All", team_select="All", date_select="All"):
    # Partimos del DF completo
    filtered = df.copy()

    # Filtrar según lo que ya haya seleccionado el usuario
    if round_select != "All":
        filtered = filtered[filtered["competition_stage"] == round_select]
    if team_select != "All":
        filtered = filtered[(filtered["home_team"] == team_select) | (filtered["away_team"] == team_select)]
    if date_select != "All":
        filtered = filtered[filtered["match_date_convert"] == date_select]

    # Listas dinámicas según lo que queda tras ese filtro
    stages_list = ["All"] + sorted(filtered["competition_stage"].unique())
    teams_list  = ["All"] + sorted(pd.concat([filtered["home_team"], filtered["away_team"]]).unique())
    dates_list  = ["All"] + sorted(filtered["match_date_convert"].unique())

    return stages_list, teams_list, dates_list


def dataframe_extraction(df, date_select="All", team_select="All", round_select="All"):
    # Partimos del DataFrame completo
    matches = df.copy()

    # Si el usuario selecciona una fecha concreta
    if date_select != "All":
        matches = matches[matches['match_date_convert'] == date_select]

    # Si selecciona un equipo concreto
    if team_select != "All":
        matches = matches[(matches['home_team'] == team_select) | (matches['away_team'] == team_select)]

    # Si selecciona una ronda concreta
    if round_select != "All":
        matches = matches[matches['competition_stage'] == round_select]

    # Ordenamos
    matches = matches.sort_values(by=['match_date_convert', 'kick_off']).reset_index(drop=True)

    # Columnas que nos interesan
    columnas_interest = [
        'match_date_convert', 'kick_off', 'home_team', 'home_score',
        'away_team', 'away_score', 'competition_stage', 'stadium',
        'referee', 'home_managers', 'away_managers'
    ]
    
    definition_info_matches = matches[columnas_interest]

    return matches, definition_info_matches



def add_team_logos(df, assets_path="./assets"):
    df = df.copy()
    df["home_logo_path"] = df["home_team"].apply(lambda t: os.path.join(assets_path, f"{t}.png").replace("\\", "/"))
    df["away_logo_path"] = df["away_team"].apply(lambda t: os.path.join(assets_path, f"{t}.png").replace("\\", "/"))
    return df



def img_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def find_coach_name(df, home= True):
    if home == True:

        coach_name= df["home_managers"].values[0]

        if pd.isna(coach_name) or coach_name == '':
            coach_name = "Not found" 

    else:
        coach_name = df["away_managers"].values[0]

        if pd.isna(coach_name) or coach_name == '':
            coach_name = "Not found" 
    
    return coach_name

def names_home_away_teams(df, match_id):
    home_name_team= df[df['match_id']==match_id]['home_team'].values[0]
    away_name_team= df[df['match_id']==match_id]['away_team'].values[0]

    return home_name_team, away_name_team
