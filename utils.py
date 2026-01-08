# utils.py
# -*- coding: utf-8 -*-

from io import BytesIO
import base64
from js import document

import pandas as pd
import os
import numpy as np

import matplotlib.pyplot as plt

import materials
from constants import *

#Remplace le savefig et envoi les figures dans un buffer que le navigateur peut afficher
def plotInJS(_fig, ):
    # mise en mémoire
    buf = BytesIO()
    _fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # conversion en base64
    img_base64 = base64.b64encode(buf.read()).decode('ascii')
    buf.close()

    # on injecte dans le div "figure"
    document.getElementById("figures").innerHTML = f'<img src="data:image/png;base64,{img_base64}" />'



def load_profile(filepath):
    #df = pd.read_csv(filepath)
    df = filepath # Avec le JS, on envoie directement un dataframe.

    if df is None:
        raise ValueError("Aucun DataFrame reçu")

    z = df.iloc[:, 0].tolist()
    xsb = (df.iloc[:, 1] / 100 / 2).tolist()

    return z, xsb



def plot_custom_compo(__linescan=False, __df_CSV_file=None):

    fig = plt.figure(figsize=(5,6))

    if __linescan == True:
        x, y = load_profile(__df_CSV_file)
        plt.ylim([0,0.6])
        plt.plot(x,y)

        plt.xlabel("Position (nm)")
        plt.ylabel("Composition (%)")

        plotInJS(fig)
    
        plt.close()



def plot_Banddiagram(params):

    fig = plt.figure(figsize=(5,6))

    db_struct = materials.prepare_heterostructure(params)
    if db_struct == -1: return -1

    if params['js_input']['flag_E_plot']: plt.plot(db_struct['z'], db_struct['Ec']/q, label="E_c")
    if params['js_input']['flag_HH_plot']: plt.plot(db_struct['z'], db_struct['Ev']/q, label="E_hh")
    if params['js_input']['flag_LH_plot']: plt.plot(db_struct['z'], db_struct['Elh']/q, label="E_lh")
    if params['js_input']['flag_SO_plot']: plt.plot(db_struct['z'], db_struct['Eso']/q, label="E_so")

    plt.xlabel("Position (nm)")
    plt.ylabel("Energy (eV)")

    E_min = params['js_input']['Emin_plot']
    E_max = params['js_input']['Emax_plot']
    plt.ylim([E_min, E_max])

    # On met juste le ternaire layer 1 si on est en mode CSV
    if params['js_input']['linescan_bool']:
        plt.title(f"{params['js_input']['mat_layer1']} from CSV file")
    else:
        plt.title(f"{params['js_input']['mat_layer1']} / {params['js_input']['mat_layer2']}")

    plt.legend()
    #plt.show()

    plotInJS(fig)
    plt.close()



def debugPlot(msg):
    fig = plt.figure(figsize=(5,6))
    plt.title(msg)

    plotInJS(fig)
    plt.close()

    return -1



def plot_dispersion(params, kspace, energies_xy, energies_z):
    # filtrage énergie pour affichage
    E_min = params['js_input']['Emin_plot']
    E_max = params['js_input']['Emax_plot']

    #if params['js_input']['linescan_bool']: E_min = -0.56; E_max = +0.2
    #else: E_min = -0.2; E_max = +0.8

    # conversion k en nm^-1 pour tracé plus lisible
    k_nm = kspace * 1e-9

    fig = plt.figure(figsize=(5,6))#, dpi=300)
    ax = plt.gca()

    # Format: -kxy (gauche, négatif) et +kz (droite, positif)
    for i, _k in enumerate(k_nm):
        # kxy à gauche : -_k ; kz à droite : +_k
        x_left = -_k ; x_right = +_k
     
        ### left part (xy, in-plane)

        Ee_xy = energies_xy['E_e'][i]
        Ehh_xy = energies_xy['E_hh'][i]
        Elh_xy = energies_xy['E_lh'][i]
        Eso_xy = energies_xy['E_so'][i]

        if params['js_input']['flag_E_plot'] and Ee_xy.size:
            ax.plot([x_left]*len(Ee_xy), Ee_xy, '.', color='k', markersize=M_SIZE)#, alpha=0.7)
        if params['js_input']['flag_HH_plot'] and Ehh_xy.size:
            ax.plot([x_left]*len(Ehh_xy), Ehh_xy, '.', color='r', markersize=M_SIZE)#, alpha=0.7)
        if params['js_input']['flag_LH_plot'] and Elh_xy.size:
            ax.plot([x_left]*len(Elh_xy), Elh_xy, '.', color='b', markersize=M_SIZE)#, alpha=0.7)
        if params['js_input']['flag_SO_plot'] and Eso_xy.size:
            ax.plot([x_left]*len(Eso_xy), Eso_xy, '.', color='g', markersize=M_SIZE)#, alpha=0.7)

        # right part (z, growth direction)

        Ee_z = energies_z['E_e'][i]
        Ehh_z = energies_z['E_hh'][i]
        Elh_z = energies_z['E_lh'][i]
        Eso_z = energies_z['E_so'][i]

        if params['js_input']['flag_E_plot'] and Ee_z.size:
            ax.plot([x_right]*len(Ee_z), Ee_z, '.', color='k', markersize=M_SIZE)
        if params['js_input']['flag_HH_plot'] and Ehh_z.size:
            ax.plot([x_right]*len(Ehh_z), Ehh_z, '.', color='r', markersize=M_SIZE)
        if params['js_input']['flag_LH_plot'] and Elh_z.size:
            ax.plot([x_right]*len(Elh_z), Elh_z, '.', color='b', markersize=M_SIZE)
        if params['js_input']['flag_SO_plot'] and Eso_z.size:
            ax.plot([x_right]*len(Eso_z), Elh_z, '.', color='g', markersize=M_SIZE)

    # esthétique
    #E_hh_0 = energies_z['E_hh'][:][0][0]
    #E_e_0 = energies_z['E_e'][::-1][len(energies_z['E_e'])-1][-1]

    #E_min = E_hh_0 - 0.2
    #E_max = E_e_0 + 0.4

    ax.set_xlim(-k_nm.max()*1.05, k_nm.max()*1.05)
    ax.set_ylim(E_min, E_max)

    ax.set_ylabel('Energy (eV)')
    ax.set_title(r'Dispersion: -$k_{xy}$ (left)  ;  +$k_{z}$ (right)')

    ax.grid(alpha=0.25)

    # légende
    if params['js_input']['flag_E_plot']: ax.plot([], [], '.', color='k', label='E')
    if params['js_input']['flag_HH_plot']: ax.plot([], [], '.', color='r', label='HH')
    if params['js_input']['flag_LH_plot']: ax.plot([], [], '.', color='b', label='LH')
    if params['js_input']['flag_SO_plot']: ax.plot([], [], '.', color='g', label='SO')
    
    ax.legend()
    plt.tight_layout()
       
    # sauvegarde en mémoire
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # convertion en base64
    img_base64 = base64.b64encode(buf.read()).decode('ascii')
    buf.close()

    # injecte dans le div "figure"
    document.getElementById("figures").innerHTML = f'<img src="data:image/png;base64,{img_base64}" />'
   
    plt.close()