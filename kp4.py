# kp4.py
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from constants import *
import utils
import materials
import band_calculations

plt.rcParams["font.family"] = "sans-serif"


def kp4(js_input, __df_CSV_file, __heterostructure_bool=False, action=""):
       
    ### Mise en forme des entrées en provenance du JS

    if js_input['linescan_bool'] == "False": js_input['linescan_bool'] = False
    if js_input['linescan_bool'] == "True": js_input['linescan_bool'] = True

    if js_input['flag_E_plot'] == "False": js_input['flag_E_plot'] = False
    if js_input['flag_E_plot'] == "True": js_input['flag_E_plot'] = True

    if js_input['flag_HH_plot'] == "False": js_input['flag_HH_plot'] = False
    if js_input['flag_HH_plot'] == "True": js_input['flag_HH_plot'] = True

    if js_input['flag_LH_plot'] == "False": js_input['flag_LH_plot'] = False
    if js_input['flag_LH_plot'] == "True": js_input['flag_LH_plot'] = True

    if js_input['flag_SO_plot'] == "False": js_input['flag_SO_plot'] = False
    if js_input['flag_SO_plot'] == "True": js_input['flag_SO_plot'] = True

    if js_input['th_layer1'] >= 0.1: js_input['th_layer1'] *= 1e-9
    if js_input['th_layer2'] >= 0.1: js_input['th_layer2'] *= 1e-9

    js_input['dz'] *= 1e-9

    if js_input['mat_layer1'] not in supported_materials: return -1
    if js_input['mat_layer2'] not in supported_materials: return -1

    #return utils.debugPlot("test")

    ### Génération de la database et mise à jour éventuelle avec les inputs utilisateurs

    layer1_database = materials.database_materials(material_name=js_input['mat_layer1'], x=js_input['x_layer1'], js_input=js_input)
    layer2_database = materials.database_materials(material_name=js_input['mat_layer2'], x=js_input['x_layer2'], js_input=js_input)

    if (action == "loadDatabase"):
        # Data à renvoyer
        #const [Gbow1, Gbow2, Vbow1, Vbow2, Dso1, Dso2, Ep1, Ep2, me1, me2, mhh1, mhh2, mlh1, mlh2, mso1, mso2] = pyResult;

        # vérifie la présence de bowing (absent en cas de binaires) et renvoie sa valeur ou 0.0
        output_to_JS = []
        if not "Gamma_bow" in layer1_database.keys(): layer1_database["Gamma_bow"] = 0.0
        if not "Gamma_bow" in layer2_database.keys(): layer2_database["Gamma_bow"] = 0.0
        if not "VB_bow" in layer1_database.keys(): layer1_database["VB_bow"] = 0.0
        if not "VB_bow" in layer2_database.keys(): layer2_database["VB_bow"] = 0.0
       
        # pour l'instant, on ne peut pas faire autrement car pyodide ne veut pas récupérer d'itérables... 
        return layer1_database["Gamma_bow"], layer2_database["Gamma_bow"], layer1_database["VB_bow"], layer2_database["VB_bow"], layer1_database["delta_so"], layer2_database["delta_so"], layer1_database["E_P"], layer2_database["E_P"], layer1_database["m_e"], layer2_database["m_e"], layer1_database["m_hh"], layer2_database["m_hh"], layer1_database["m_lh"], layer2_database["m_lh"], layer1_database["m_so"], layer2_database["m_so"]


    else:
        # Si on ne charge pas la database du python vers le JS, alors on fait l'inverse, on charge les valeurs utilisateurs
        # depuis le JS vers le Python.

        layer1_updates = {
            'E_P': js_input['Ep_1'],
            'delta_so': js_input['D_SO_1'],
            'Gamma_bow': js_input['Gamma_bow_1'],
            'VB_bow': js_input['Vb_bow_1'],
            'm_e': js_input['me_1'],
            'm_hh': js_input['mhh_1'],
            'm_lh': js_input['mlh_1'],
            'm_so': js_input['mso_1'],
        }

        layer2_updates = {
            'E_P': js_input['Ep_2'],
            'delta_so': js_input['D_SO_2'],
            'Gamma_bow': js_input['Gamma_bow_2'],
            'VB_bow': js_input['Vb_bow_2'],
            'm_e': js_input['me_2'],
            'm_hh': js_input['mhh_2'],
            'm_lh': js_input['mlh_2'],
            'm_so': js_input['mso_2'],
        }

        layer1_database = materials.database_materials(material_name=js_input['mat_layer1'], x=js_input['x_layer1'], js_input=js_input, update_values=layer1_updates)
        layer2_database = materials.database_materials(material_name=js_input['mat_layer2'], x=js_input['x_layer2'], js_input=js_input, update_values=layer2_updates)


    # Options utiles pour le Python
    py_vars = {
        'CSV_file': __df_CSV_file,
        'debug_counts': 0,
        'proj_threshold': 0.5,   # 0.53 ?
        'plot_heterostructure': __heterostructure_bool,
    }

    # params global avec les entrée JS, les options PY et la database de chaque couche.
    params = {
        'js_input': js_input,
        'py_vars': py_vars,
        'db_layer1': layer1_database,
        'db_layer2': layer2_database,
    }

    
    # Si on veut seulement calculer le diagramme de bandes de l'hététérostructure
    if params['py_vars']['plot_heterostructure']:
        err = utils.plot_Banddiagram(params=params)
        return err
    
    
    # Sinon, balayage kspace

    d = params['js_input']['th_layer1'] + params['js_input']['th_layer2'] # SL period
    kspace = np.linspace(0.0, np.pi/d, params['js_input']['nk']) # 1/m

    ### Sweep xy, puis z.
    energies_xy = band_calculations.start_k_sweep(params=params, sweepType="xy", k_range=kspace)
    energies_z = band_calculations.start_k_sweep(params=params, sweepType="z", k_range=kspace)

    ### Plot de la disperison
    utils.plot_dispersion(params, kspace, energies_xy, energies_z)
    

    ### Calcule des masses effectives
    # on supprime les derniers éléments xy et on joint les listes (kxy=kz=0)
    k_range = [kspace[0], kspace[1], kspace[2], kspace[3], kspace[4]]

    e_e_z = energies_z['E_e']
    e_hh_z = energies_z['E_hh']
    e_lh_z = energies_z['E_lh']
    e_e_xy = energies_xy['E_e']
    e_hh_xy = energies_xy['E_hh']
    e_lh_xy = energies_xy['E_lh']

    e_band_z = band_calculations.energies_around_Gamma(energies=e_e_z, band_type="conduction")
    hh_band_z = band_calculations.energies_around_Gamma(energies=e_hh_z, band_type="valence")
    lh_band_z = band_calculations.energies_around_Gamma(energies=e_lh_z, band_type="valence")
    e_band_xy = band_calculations.energies_around_Gamma(energies=e_e_xy, band_type="conduction")
    hh_band_xy = band_calculations.energies_around_Gamma(energies=e_hh_xy, band_type="valence")
    lh_band_xy = band_calculations.energies_around_Gamma(energies=e_lh_xy, band_type="valence")

    meff_fitted_hh_z, meff_fitted_lh_z, meff_fitted_e_z, meff_fitted_hh_xy, meff_fitted_lh_xy, meff_fitted_e_xy = [
        band_calculations.estimate_effective_mass(k_range, _band) for _band in [hh_band_z, lh_band_z, e_band_z,
                                                                                hh_band_xy, lh_band_xy, e_band_xy]
    ]
    
    Egap = round(1e3 * (e_e_z[::-1][len(e_e_z)-1][-1] - e_hh_z[:][0][0]), 2)
    delta_hh_lh = round(1e3 * (e_hh_z[:][0][0] - e_lh_z[:][0][0]), 2)

    ##############################################################################

    return meff_fitted_hh_z, meff_fitted_lh_z, meff_fitted_e_z, meff_fitted_hh_xy, meff_fitted_lh_xy, meff_fitted_e_xy, Egap, delta_hh_lh

if __name__ == "__main__":
    pass