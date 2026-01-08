# materials.py
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from constants import *
import utils 


def calculate_bandgap(eg0, alpha, beta, temp):
    Egap_T = eg0 - alpha*(temp**2) / (temp+beta)
    return Egap_T



def database_materials(material_name, x, js_input, update_values={}):

    T = js_input['temperature']

    # Potentiel de référence fixé pour être celui de la BV de l'InAs, et éviter d'avoir à recentrer l'affichage dans la plupart des cas.
    # On applique ensuite Ev - REF_POTENTIAL à toutes les entrées database, pour toutes les valeurs de 'supported_materials'.
    REF_POTENTIAL = 1.39 # eV

    database = {}
    ###############################################################################################


    """
    ----------
    -- GaAs --
    ----------
    """
    database['GaAs'] = {
        'm_e':              0.067,          #Vurgaftman2001
        'Eg_0K':            1.519,          #Vurgaftman2001
        'Eg_alpha':         0.5405e-3,      #Vurgaftman2001
        'Eg_beta':          204,            #Vurgaftman2001
        'Ev':               1.346,          #Zunger
        'm_hh':             0.51,           #http://www.ioffe.ru/SVA/NSM/Semicond/GaAs/bandstr.html
        'm_lh':             0.082,          #http://www.ioffe.ru/SVA/NSM/Semicond/GaAs/bandstr.html
        'm_so':             0.172,          #Vurgaftman2001
        'delta_so':         0.341,          #Vurgaftman2001
        'E_P':              28.8,           #Vurgaftman2001
    }
    ###############################################################################################


    """
    ----------
    -- AlAs --
    ----------
    """
    database['AlAs'] = {
        'm_e':              0.15,           #Vurgaftman2001
        'Eg_0K':            3.099,          #Vurgaftman2001
        'Eg_alpha':         0.885e-3,       #Vurgaftman2001
        'Eg_beta':          530,            #Vurgaftman2001
        'Ev':               0.857,          #Zunger
        'm_hh':             0.5,            #Landolt-Boernstein
        'm_lh':             0.26,           #Landolt-Boernstein
        'm_so':             0.28,           #Vurgaftman2001
        'delta_so':         0.28,           #Vurgaftman2001
        'E_P':              21.1,           #Vurgaftman2001
    }
    ###############################################################################################


    """
    ----------
    -- InAs --
    ----------
    """
    database['InAs'] = {
        'm_e':              0.026,          #Vurgaftman2001
        'Eg_0K':            0.417,          #Vurgaftman2001
        'Eg_alpha':         0.276e-3,       #Vurgaftman2001
        'Eg_beta':          93,             #Vurgaftman2001
        'Ev':               1.39,           #Zunger
        'm_hh':             0.41,           #http://www.ioffe.ru/SVA/NSM/Semicond/InAs/bandstr.html
        'm_lh':             0.026,          #Yu, Cardona, Fundamentals of Semiconductors, p. 70, http://www.ioffe.ru/SVA/NSM/Semicond/InAs/bandstr.html
        'm_so':             0.14,           #Vurgaftman2001
        'delta_so':         0.39,           #Vurgaftman2001
        'E_P':              21.5,           #Vurgaftman2001
    }
    ###############################################################################################


    """
    ----------
    -- GaSb --
    ----------
    """
    database['GaSb'] = {
        'm_e':              0.039,          #Vurgaftman2001
        'Eg_0K':            0.812,          #Vurgaftman2001
        'Eg_alpha':         0.417e-3,       #Vurgaftman2001
        'Eg_beta':          140,            #Vurgaftman2001
        'Ev':               1.777,          #Zunger
        'm_hh':             0.34,           #Landolt-Boernstein
        'm_lh':             0.0447,         #Landolt-Boernstein
        'm_so':             0.12,           #Vurgaftman2001
        'delta_so':         0.76,           #Vurgaftman2001
        'E_P':              27.0,           #Vurgaftman2001
    }
    ###############################################################################################


    """
    ----------
    -- AlSb --
    ----------
    """
    database['AlSb'] = {
        'm_e':              0.14,           #Vurgaftman2001
        'Eg_0K':            2.386,          #Vurgaftman2001
        'Eg_alpha':         0.42e-3,        #Vurgaftman2001
        'Eg_beta':          140,            #Vurgaftman2001
        'Ev':               1.385,          #Zunger
        'm_hh':             0.8,            #Landolt-Boernstein
        'm_lh':             0.13,           #Landolt-Boernstein
        'm_so':             0.22,           #Vurgaftman2001
        'delta_so':         0.676,          #Vurgaftman2001
        'E_P':              18.7,           #Vurgaftman2001
    }
    ###############################################################################################


    """
    ----------
    -- InSb --
    ----------
    """
    database['InSb'] = {
        'm_e':              0.0135,         #Vurgaftman2001
        'Eg_0K':            0.235,          #Vurgaftman2001
        'Eg_alpha':         0.32e-3,        #Vurgaftman2001
        'Eg_beta':          170,            #Vurgaftman2001
        'Ev':               1.750,          #Zunger
        'm_hh':             0.405,          #Landolt-Boernstein
        'm_lh':             0.0162,         #Landolt-Boernstein
        'm_so':             0.11,           #Vurgaftman2001
        'delta_so':         0.81,           #Vurgaftman2001
        'E_P':              23.3,           #Vurgaftman2001
    }
    ###############################################################################################


    """
    --------------------
    -- In(1-x)Ga(x)As --
    --------------------
    """
    database['In(1-x)Ga(x)As'] = {}
    for key in database['InAs'].keys():
        database['In(1-x)Ga(x)As'][key] = database['InAs'][key]*(1-x) + database['GaAs'][key]*x

    database['In(1-x)Ga(x)As']['Gamma_bow'] = 0.477 #Vurgaftman2001
    database['In(1-x)Ga(x)As']['Eg_0K'] -= x*(1-x) * database['In(1-x)Ga(x)As']['Gamma_bow']
    database['In(1-x)Ga(x)As']['VB_bow'] = -0.43 #Vurgaftman2001
    database['In(1-x)Ga(x)As']['Ev'] -= x*(1-x) * database['In(1-x)Ga(x)As']['VB_bow']
    database['In(1-x)Ga(x)As']['Ep_bow'] = -1.48 #Vurgaftman2001
    database['In(1-x)Ga(x)As']['E_P'] -= x*(1-x) * database['In(1-x)Ga(x)As']['Ep_bow']
    database['In(1-x)Ga(x)As']['m_e_bow'] = 0.0091 #Vurgaftman2001
    database['In(1-x)Ga(x)As']['m_e'] -= x*(1-x) * database['In(1-x)Ga(x)As']['m_e_bow']
    database['In(1-x)Ga(x)As']['m_hh_bow'] = -0.145 #Vurgaftman2001
    database['In(1-x)Ga(x)As']['m_hh'] -= x*(1-x) * database['In(1-x)Ga(x)As']['m_hh_bow']
    database['In(1-x)Ga(x)As']['m_lh_bow'] = 0.0202 #Vurgaftman2001
    database['In(1-x)Ga(x)As']['m_lh'] -= x*(1-x) * database['In(1-x)Ga(x)As']['m_lh_bow']
    database['In(1-x)Ga(x)As']['delta_so_bow'] = 0.15 #Vurgaftman2001
    database['In(1-x)Ga(x)As']['delta_so'] -= x*(1-x) * database['In(1-x)Ga(x)As']['delta_so_bow']
    ###############################################################################################


    """
    ---------------------
    -- Ga(1-x)In(x)Sb ---
    ---------------------
    """
    database['Ga(1-x)In(x)Sb'] = {}
    for key in database['GaSb'].keys():
        database['Ga(1-x)In(x)Sb'][key] = database['GaSb'][key]*(1-x) + database['InSb'][key]*x

    database['Ga(1-x)In(x)Sb']['m_e_bow'] = 0.0092 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['m_e'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['m_e_bow']
    database['Ga(1-x)In(x)Sb']['Gamma_bow'] = 0.415 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['Eg_0K'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['Gamma_bow']
    database['Ga(1-x)In(x)Sb']['m_lh_bow'] = 0.011 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['m_lh'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['m_lh_bow']
    database['Ga(1-x)In(x)Sb']['VB_bow'] = -0.03333 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['Ev'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['VB_bow']
    database['Ga(1-x)In(x)Sb']['delta_so_bow'] = 0.1 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['delta_so'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['delta_so_bow']
    ###############################################################################################


    """
    ---------------------
    -- InAs(1-x)Sb(x) ---
    ---------------------
    """
    database['InAs(1-x)Sb(x)'] = {}
    for key in database['InSb'].keys():
        database['InAs(1-x)Sb(x)'][key] = database['InAs'][key]*(1-x) + database['InSb'][key]*x

    database['InAs(1-x)Sb(x)']['m_e_bow'] = 0.035 #Vurgaftman2001
    database['InAs(1-x)Sb(x)']['m_e'] -= x*(1-x) * database['InAs(1-x)Sb(x)']['m_e_bow']
    database['InAs(1-x)Sb(x)']['Gamma_bow'] = 0.67 #Vurgaftman2001
    database['InAs(1-x)Sb(x)']['Eg_0K'] -= x*(1-x) * database['InAs(1-x)Sb(x)']['Gamma_bow']
    database['InAs(1-x)Sb(x)']['VB_bow'] = -0.4 #Vurgaftman2001
    database['InAs(1-x)Sb(x)']['Ev'] -= x*(1-x) * database['InAs(1-x)Sb(x)']['VB_bow']
    database['InAs(1-x)Sb(x)']['delta_so_bow'] = 1.2 #Vurgaftman2001
    database['InAs(1-x)Sb(x)']['delta_so'] -= x*(1-x) * database['InAs(1-x)Sb(x)']['delta_so_bow']
    ###############################################################################################


    """
    ---------------------
    -- Al(1-x)Ga(x)As ---
    ---------------------
    """
    database['Al(1-x)Ga(x)As'] = {}
    for key in database['AlAs'].keys():
        database['Al(1-x)Ga(x)As'][key] = database['AlAs'][key]*(1-x) + database['GaAs'][key]*x

    database['Al(1-x)Ga(x)As']['Gamma_bow'] = 1.183*x + (1-x)*-0.127 #Vurgaftman2001 #bowing lui-même variable en x
    database['Al(1-x)Ga(x)As']['Eg_0K'] -= x*(1-x) * database['Al(1-x)Ga(x)As']['Gamma_bow']
    ###############################################################################################


    """
    ---------------------
    -- Al(1-x)In(x)As ---
    ---------------------
    """
    database['Al(1-x)In(x)As'] = {}
    for key in database['AlAs'].keys():
        database['Al(1-x)In(x)As'][key] = database['AlAs'][key]*(1-x) + database['InAs'][key]*x

    database['Al(1-x)In(x)As']['m_e_bow'] = 0.049 #Vurgaftman2001
    database['Al(1-x)In(x)As']['m_e'] -= x*(1-x) * database['Al(1-x)In(x)As']['m_e_bow']
    database['Al(1-x)In(x)As']['Gamma_bow'] = 0.70 #Vurgaftman2001
    database['Al(1-x)In(x)As']['Eg_0K'] -= x*(1-x) * database['Al(1-x)In(x)As']['Gamma_bow']
    database['Al(1-x)In(x)As']['VB_bow'] = -0.64 #Vurgaftman2001
    database['Al(1-x)In(x)As']['Ev'] -= x*(1-x) * database['Al(1-x)In(x)As']['VB_bow']
    database['Al(1-x)In(x)As']['delta_so_bow'] = 0.15 #Vurgaftman2001
    database['Al(1-x)In(x)As']['delta_so'] -= x*(1-x) * database['Al(1-x)In(x)As']['delta_so_bow']
    database['Al(1-x)In(x)As']['Ep_bow'] = -4.81 #Vurgaftman2001
    database['Al(1-x)In(x)As']['E_P'] -= x*(1-x) * database['In(1-x)Ga(x)As']['Ep_bow']
    ###############################################################################################


    """
    ---------------------
    -- Al(1-x)In(x)Sb ---
    ---------------------
    """
    database['Al(1-x)In(x)Sb'] = {}
    for key in database['AlAs'].keys():
        database['Al(1-x)In(x)Sb'][key] = database['AlAs'][key]*(1-x) + database['InSb'][key]*x

    database['Al(1-x)In(x)Sb']['Gamma_bow'] = 0.43 #Vurgaftman2001
    database['Al(1-x)In(x)Sb']['Eg_0K'] -= x*(1-x) * database['Al(1-x)In(x)Sb']['Gamma_bow']
    database['Al(1-x)In(x)Sb']['VB_bow'] = -0.08333 #Vurgaftman2001
    database['Al(1-x)In(x)Sb']['Ev'] -= x*(1-x) * database['Al(1-x)In(x)Sb']['VB_bow']
    database['Al(1-x)In(x)Sb']['delta_so_bow'] = 0.25 #Vurgaftman2001
    database['Al(1-x)In(x)Sb']['delta_so'] -= x*(1-x) * database['Al(1-x)In(x)Sb']['delta_so_bow']
    ###############################################################################################


    """
    ---------------------
    -- AlAs(1-x)Sb(x) ---
    ---------------------
    """
    database['AlAs(1-x)Sb(x)'] = {}
    for key in database['AlAs'].keys():
        database['AlAs(1-x)Sb(x)'][key] = database['AlAs'][key]*(1-x) + database['AlSb'][key]*x

    database['AlAs(1-x)Sb(x)']['Gamma_bow'] = 0.8 #Vurgaftman2001
    database['AlAs(1-x)Sb(x)']['Eg_0K'] -= x*(1-x) * database['AlAs(1-x)Sb(x)']['Gamma_bow']
    database['AlAs(1-x)Sb(x)']['VB_bow'] = -1.76 #Vurgaftman2001
    database['AlAs(1-x)Sb(x)']['Ev'] -= x*(1-x) * database['AlAs(1-x)Sb(x)']['VB_bow']
    database['AlAs(1-x)Sb(x)']['delta_so_bow'] = 0.15 #Vurgaftman2001
    database['AlAs(1-x)Sb(x)']['delta_so'] -= x*(1-x) * database['AlAs(1-x)Sb(x)']['delta_so_bow']
    ###############################################################################################


    """
    ---------------------
    -- Al(1-x)Ga(x)Sb ---
    ---------------------
    """
    database['Al(1-x)Ga(x)Sb'] = {}
    for key in database['AlAs'].keys():
        database['Al(1-x)Ga(x)Sb'][key] = database['AlSb'][key]*(1-x) + database['GaSb'][key]*x

    database['Al(1-x)Ga(x)Sb']['Gamma_bow'] = -0.044*x + (1-x)*1.264 #Vurgaftman2001 #bowing lui-même variable en x
    database['Al(1-x)Ga(x)Sb']['Eg_0K'] -= x*(1-x) * database['Al(1-x)Ga(x)Sb']['Gamma_bow']
    database['Al(1-x)Ga(x)Sb']['VB_bow'] = -0.1 #Vurgaftman2001
    database['Al(1-x)Ga(x)Sb']['Ev'] -= x*(1-x) * database['Al(1-x)Ga(x)Sb']['VB_bow']
    database['Al(1-x)Ga(x)Sb']['delta_so_bow'] = 0.3 #Vurgaftman2001
    database['Al(1-x)Ga(x)Sb']['delta_so'] -= x*(1-x) * database['Al(1-x)Ga(x)Sb']['delta_so_bow']
    ###############################################################################################


    """
    ---------------------
    -- GaAs(1-x)Sb(x) ---
    ---------------------
    """
    database['GaAs(1-x)Sb(x)'] = {}
    for key in database['AlAs'].keys():
        database['GaAs(1-x)Sb(x)'][key] = database['GaAs'][key]*(1-x) + database['GaSb'][key]*x

    database['GaAs(1-x)Sb(x)']['Gamma_bow'] = 1.43 #Vurgaftman2001
    database['GaAs(1-x)Sb(x)']['Eg_0K'] -= x*(1-x) * database['GaAs(1-x)Sb(x)']['Gamma_bow']
    database['GaAs(1-x)Sb(x)']['VB_bow'] = -1.26 #Vurgaftman2001
    database['GaAs(1-x)Sb(x)']['Ev'] -= x*(1-x) * database['GaAs(1-x)Sb(x)']['VB_bow']
    database['GaAs(1-x)Sb(x)']['delta_so_bow'] = 0.6 #Vurgaftman2001
    database['GaAs(1-x)Sb(x)']['delta_so'] -= x*(1-x) * database['GaAs(1-x)Sb(x)']['delta_so_bow']
    ###############################################################################################


    """
    ---------------------
    -- Ga(1-x)In(x)Sb ---
    ---------------------
    """
    database['Ga(1-x)In(x)Sb'] = {}
    for key in database['AlAs'].keys():
        database['Ga(1-x)In(x)Sb'][key] = database['GaSb'][key]*(1-x) + database['InSb'][key]*x

    database['Ga(1-x)In(x)Sb']['m_e_bow'] = 0.0092 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['m_e'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['m_e_bow']
    database['Ga(1-x)In(x)Sb']['Gamma_bow'] = 0.415 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['Eg_0K'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['Gamma_bow']
    database['Ga(1-x)In(x)Sb']['m_lh_bow'] = 0.011 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['m_lh'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['m_lh_bow']
    database['Ga(1-x)In(x)Sb']['VB_bow'] = -0.03333 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['Ev'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['VB_bow']
    database['Ga(1-x)In(x)Sb']['delta_so_bow'] = 0.1 #Vurgaftman2001
    database['Ga(1-x)In(x)Sb']['delta_so'] -= x*(1-x) * database['Ga(1-x)In(x)Sb']['delta_so_bow']

    ###############################################################################################

    # Prise en compte du REF_POTENTIAL pour centrer l'affichage.
    for mat_name in supported_materials:
        database[mat_name]['Ev'] -= REF_POTENTIAL
    
    # Calcul du gap en température, de la position du Ec, et ajout dans le database à renvoyer.
    database[material_name]['Eg_T'] = calculate_bandgap(database[material_name]['Eg_0K'], database[material_name]['Eg_alpha'], database[material_name]['Eg_beta'], T)

    ####### UPDATE FROM JS USER VALUES
    if update_values != {}:
        for key in update_values.keys():
            # met à jour la db de chaque layer avec les inputs utilisateurs
            database[material_name][key] = update_values[key]

        # finalement on recalcule ce qu'il faut avec les nouveaux bowings
        database[material_name]['Eg_0K'] -= x*(1-x) * database[material_name]['Gamma_bow']
        database[material_name]['Ev'] -= x*(1-x) * database[material_name]['VB_bow']

    database[material_name]['Ec'] = database[material_name]['Ev'] + database[material_name]['Eg_T']


    return database[material_name]



def prepare_heterostructure(params):
    heterostructure_data = {}

    # si activé, on n'utilise pas les paramètres entrées et on passe
    # en mode linescan pour déterminer les paramètres dépendant de la position.
    if params['js_input']['linescan_bool'] == True:

        """ ############################
        Attention toute cette partie n'est pas aussi à jour que la version à 2 couches !!!

        """ ############################

        # on vérifie que le matériau layer1 est bien un ternaire, autrement fonction ne marche pas encore
        if "(x)" not in params['js_input']['mat_layer1']: return -1

        #file = 'C:/Users/user1/Desktop/1_SIMULATION/NEXTNANO/tem2bands/data/profiles/E1100.csv'
        file = params['py_vars']['CSV_file']
        z, xsb = utils.load_profile(file)

        if 0: # raw plot
            plt.plot(z, xsb); plt.show()

        # InAsSb remplacé pour récupérer le ternaire en layer1
        #custom_params = [params_for_InAsSb(_x, params['bowing_Eg'], params['bowing_Ev']) for _x in xsb]
        custom_params = [database_materials(  material_name=params['js_input']['mat_layer1'],
                                              x=_x,
                                              js_input=params['js_input'] )
                        for _x in xsb]

        period_SL = round(max(z) * 1e-9, 12)
        Nz = len(z)
        dz = period_SL / Nz
        
        # On force le réagencement des z pour garantir un dz fixe.
        z = np.arange(Nz) * dz
        
        Ec = np.zeros(Nz, dtype=float)
        Ev = np.zeros(Nz, dtype=float)
        Elh = np.zeros(Nz, dtype=float)
        Eso = np.zeros(Nz, dtype=float)
        d_SO = np.zeros(Nz, dtype=float)
        Ep_eV = np.zeros(Nz, dtype=float)
        m_e = np.zeros(Nz, dtype=float)
        m_hh = np.zeros(Nz, dtype=float)
        m_lh = np.zeros(Nz, dtype=float)
        m_so = np.zeros(Nz, dtype=float)
        
        dstrain_layer1 = params['js_input']['delta_strain_layer1']
        
        for i in range(Nz):
            Ec[i] = custom_params[i]['Ec'] * q
            Ev[i] = custom_params[i]['Ev'] * q
            Elh[i] = (custom_params[i]['Ev'] + dstrain_layer1) * q
            
            d_SO[i] = custom_params[i]['delta_so'] * q
            Ep_eV[i] = custom_params[i]['E_P'] * q
            
            m_e[i] = custom_params[i]['m_e'] * m0
            m_hh[i] = custom_params[i]['m_hh'] * m0
            m_lh[i] = custom_params[i]['m_lh'] * m0
            m_so[i] = custom_params[i]['m_so'] * m0
            
            
        for i in range(Nz):
            Eso[i] = Ec[i] - d_SO[i]
            
            
        # Couplages Kane
        Ep_J = Ep_eV * q
        P_array = np.sqrt(Ep_J * (hbar**2) / (2.0 * m0))
        P_diag = np.diag(P_array)
        
       
    
    else:    
        # paramètres matériaux (en SI quand nécessaire)

        dz_user = params['js_input']['dz']
        th_layer1 = params['js_input']['th_layer1']
        th_layer2 = params['js_input']['th_layer2']

        period_SL = round(th_layer1 + th_layer2, 12)

        # forcer Nz entier puis recalcule dz pour cohérence
        Nz = int(np.round(period_SL / dz_user))
        if Nz < 4:
            Nz = max(4, Nz)
        dz = period_SL / Nz
        z = np.arange(Nz) * dz

        # bandes et potentiels (en J)
        d_strain_layer1 = params['js_input']['delta_strain_layer1'] * q
        d_strain_layer2 = params['js_input']['delta_strain_layer2'] * q
    
        Ec_layer1 = params['db_layer1']['Ec']*q
        Ec_layer2 = params['db_layer2']['Ec']*q
        Ev_layer1 = params['db_layer1']['Ev']*q
        Ev_layer2 = params['db_layer2']['Ev']*q
        SO_layer1 = params['db_layer1']['delta_so']*q
        SO_layer2 = params['db_layer2']['delta_so']*q

        # masses (en kg)
        me_layer1 = params['db_layer1']['m_e']*m0
        me_layer2 = params['db_layer2']['m_e']*m0
        mhh_layer1 = params['db_layer1']['m_hh']*m0
        mhh_layer2 = params['db_layer2']['m_hh']*m0
        mlh_layer1 = params['db_layer1']['m_lh']*m0
        mlh_layer2 = params['db_layer2']['m_lh']*m0
        mso_layer1 = params['db_layer1']['m_so']*m0
        mso_layer2 = params['db_layer2']['m_so']*m0

        """
        Ec = np.where(z < th_layer1, Ec_layer1 - d_strain_layer1, Ec_layer2 - d_strain_layer2)
        Ev = np.where(z < th_layer1, Ev_layer1 - d_strain_layer1, Ev_layer2 - d_strain_layer2)
        Elh = np.where(z < th_layer1, Ev_layer1, Ev_layer2)
        Eso = np.where(z < th_layer1, Ev_layer1 - d_strain_layer1 - SO_layer1, Ev_layer2 - d_strain_layer2 - SO_layer2)
        """

        # On positionne les niveaux par rapport à Ev (HH)
        Ev = np.where(z < th_layer1, Ev_layer1, Ev_layer2)
        Ec = np.where(z < th_layer1, Ec_layer1, Ec_layer2)
        Elh = np.where(z < th_layer1, Ev_layer1 + d_strain_layer1, Ev_layer2 + d_strain_layer2)
        Eso = np.where(z < th_layer1, Ev_layer1 + d_strain_layer1 - SO_layer1, Ev_layer2 + d_strain_layer2 + SO_layer2)

        m_e = np.where(z < th_layer1, me_layer1, me_layer2)
        m_hh = np.where(z < th_layer1, mhh_layer1, mhh_layer2)
        m_lh = np.where(z < th_layer1, mlh_layer1, mlh_layer2)
        m_so = np.where(z < th_layer1, mso_layer1, mso_layer2)
        
        # Couplages Kane
        Ep_J = np.where(z < th_layer1, params['db_layer1']['E_P']*q, params['db_layer2']['E_P']*q)
        # P_SI tel que Ep = 2*m0*P^2 / hbar^2  -> P = sqrt(Ep * hbar^2 / (2*m0))
        P_SI = np.sqrt(Ep_J * (hbar**2) / (2.0 * m0))
        P_array = np.full(Nz, P_SI)
        P_diag = np.diag(P_array)


    ####################

    heterostructure_data['m_e'] = m_e
    heterostructure_data['m_hh'] = m_hh
    heterostructure_data['m_lh'] = m_lh
    heterostructure_data['m_so'] = m_so

    heterostructure_data['Ec'] = Ec
    heterostructure_data['Ev'] = Ev
    heterostructure_data['Elh'] = Elh
    heterostructure_data['Eso'] = Eso

    heterostructure_data['P_array'] = P_array
    heterostructure_data['P_diag'] = P_diag

    heterostructure_data['z'] = z
    heterostructure_data['Nz'] = Nz
    heterostructure_data['period_SL'] = period_SL
    heterostructure_data['dz'] = dz

    return heterostructure_data