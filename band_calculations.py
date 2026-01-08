# band_calculations.py
# -*- coding: utf-8 -*-

import numpy as np

from scipy.linalg import eigh

from constants import *
import materials

#pas utilisable avec pyodide
#from findiff import Diff 


def energies_around_Gamma(energies=[], band_type=""):
    ## Les énergies en BV sont triées dans le sens décroissant et
    ## celles en BC dans le sens croissant, donc on ajuste en fonction.

    if (band_type == "valence"):
        band = [energies[:][0][0]*q, 
                energies[:][1][0]*q, 
                energies[:][2][0]*q,
                energies[:][3][0]*q,
                energies[:][4][0]*q]

    elif (band_type == "conduction"):
        N_elem = len(energies)

        band = [energies[::-1][N_elem-1][-1]*q, 
                energies[::-1][N_elem-2][-1]*q, 
                energies[::-1][N_elem-3][-1]*q,
                energies[::-1][N_elem-4][-1]*q,
                energies[::-1][N_elem-5][-1]*q]

    return band


# estimation masse effective par fit quadratique autour du centre
def estimate_effective_mass(k_list, E_list):
    mid = 3 # point indice central
    
    ksub = k_list[mid-2:mid+3]
    Esub = E_list[mid-2:mid+3]
    
    coeffs = np.polyfit(ksub, Esub, 2)
    m_eff = abs(hbar**2 / (2.0 * coeffs[0])) / m0

    return round(m_eff, 3)


# normalisation des fonctions d'onde
def normalized_wavefunctions(psi, dz):
    norm = np.sqrt(np.sum(np.abs(psi)**2) * dz)
    vecs_norm = psi / norm

    return vecs_norm


# calcul de la probabilité d'un état sur toutes les eigenvalues
def proba_wavefunctions(psi_norm, dz):
    return np.sum(np.abs(psi_norm)**2) * dz



def compute_projections_and_labels(E, psi, Nz, params):
    dz = params['js_input']['dz']
    threshold = params['py_vars']['proj_threshold']
    
    n_eigenvalues = psi.shape[1] # psi de taille 4*Nz

    # 4 composantes : E / HH / LH / SO
    # chacune dicrétisée en Nz points
    proba_per_Nz = np.zeros((n_eigenvalues, 4))

    labels = np.full(n_eigenvalues, -1, dtype=int)
    
    for i in range(n_eigenvalues):
        psi_vecs = psi[:, i]
        psi_vecs_norm = normalized_wavefunctions(psi_vecs, dz)

        #####

        psi_e = psi_vecs_norm[0:Nz]
        proba_e = proba_wavefunctions(psi_e, dz)

        psi_hh = psi_vecs_norm[Nz:2*Nz]
        proba_hh = proba_wavefunctions(psi_hh, dz)

        psi_lh = psi_vecs_norm[2*Nz:3*Nz]
        proba_lh = proba_wavefunctions(psi_lh, dz)

        psi_so = psi_vecs_norm[3*Nz:4*Nz]
        proba_so = proba_wavefunctions(psi_so, dz)

        proba_per_Nz[i,:] = [proba_e, proba_hh, proba_lh, proba_so]

        dominant = np.argmax(proba_per_Nz[i,:])
        if proba_per_Nz[i, dominant] >= threshold:
            labels[i] = dominant
        else:
            labels[i] = -1
    return proba_per_Nz, labels



def first_derivative(Nz, dz, kz, period):
    # on construit un opérateur dérivée 1ère en approximant
    # df/dz ~= [f(i+1) - f(i-1) ] / (2*dz) (différences finies centrées)
    # donc avec un coeff. +1/2dz à droite et -1/2dz à gauche
    # D1 = 1/2dz * (1..-1..1..-1)

    # Autres refs : https://github.com/maroba/findiff
    # https://github.com/zaman13/Matrix-Differentiation-Operators/blob/master/Code/diff_matrices.py

    D1 = np.zeros((Nz, Nz), dtype=complex)

    imax = Nz - 1

    D1[imax, 0] = 1.0/(2*dz)
    D1[0, imax] = -1.0/(2*dz)

    # points intérieurs
    for i in range(Nz):
        # voisin de droite
        if i != imax:
            D1[i, i+1] = +1 * 1.0/(2*dz)            

        # voisin de gauche
        if i != 0:
            D1[i, i-1] = -1 * 1.0/(2*dz)            


    phase = np.exp(1j * kz * period)

    D1[imax, 0] *= phase
    D1[0, imax] *= np.conj(phase)

    return D1



def build_BenDanielDuke_mx(m_z, Nz, dz, kz, period):
    M = np.zeros((Nz, Nz), dtype=complex)
    imax = Nz - 1
    
    # Ben Daniel-Duke : m(z) comme traité comme variable + continuité
    # de la phase de Bloch

    # On remplace les masses locales m[i] par leur moyenne avec m[i+1] pour
    # assurer la continuité de la masse effective entre les interfaces (voir
    # Bastard p.74 et Appendix A. Boundary conditions and stationnary states)
    # Conditions aux limites (x=0 et x=Nz) inchangées.
    # https://arxiv.org/html/2508.07792v1

    m_z_moy = np.zeros(Nz)
    for i in range(Nz):
        #if i == 0 or i == xmax: # conditions aux bords
        if i == imax:
            m_z_moy[i] = (m_z[i] + m_z[0]) / 2 # m[0] est la première valeur de la couche suivante => continuité
        else: # pondération pour lisser les interfaces abruptes
            m_z_moy[i] = (m_z[i] + m_z[(i+1)]) / 2


    pref = (hbar**2)/2 /(dz**2)


    ### conditions aux limites périodiques voisins droite/gauche

    # cond. limites diagonale
    M[0, 0] = pref * (1/m_z_moy[0] + 1/m_z_moy[imax])

    #cond. limites voisins de droite/gauche
    M[imax, 0] = -pref * (1/m_z_moy[imax])
    M[0, imax] = -pref * (1/m_z_moy[imax])

    # remplissage diagonal hors boundaries pour voisins gauche/droite
    for i in range(Nz): 
        # diagonale
        M[i, i] = pref * (1/m_z_moy[i] + 1/m_z_moy[i-1])
            
        # voisin de gauche
        if i != 0:
            M[i, i-1] = -pref * (1/m_z_moy[i-1]) 
        # voisin de droite
        if i != imax:
            M[i, i+1] = -pref * (1/m_z_moy[i])


    # on applique Bloch aux limites en plus de la continuité BDD
    phase = np.exp(1j * kz * period)

    M[imax, 0] *= phase # phase au début de la période (donc voisin de droite équivalent à point 0)
    M[0, imax] *= np.conj(phase) # déphasage à la fin de la période (donc point à gauche équivalent à imax période précédente)

    return M



def build_kp4_hamiltonian(kx, ky, kz, params):
    # Construit la matrice 4*Nz x 4*Nz de l'hétérostructure pour
    # un k(x,y,z) donné.
    
    data = materials.prepare_heterostructure(params)

    m_e = data['m_e']
    m_hh = data['m_hh']
    m_lh = data['m_lh']
    m_so = data['m_so']

    Ec  = data['Ec']
    Ev  = data['Ev']
    Elh = data['Elh']
    Eso = data['Eso']

    P_array = data['P_array']

    ### A ce moment, toutes les listes précédentes sont des tableaux (1 x Nz)

    P_diag  = data['P_diag']

    ### On met sous forme diagonale P_array, ce qui fait donc une matrice (Nz x Nz),
    ### Avec seulement les diagonales (indices [i,i]) remplies.

    Nz        = data['Nz']
    period_SL = data['period_SL']
    dz        = data['dz']

    ###############

    # matrices diagonales et opérateurs ordinaires
    zeros = np.zeros((Nz, Nz), dtype=complex)

    # e- conduction
    diag_e_kxy = (hbar**2 * (kx**2 + ky**2)) / (2.0*m_e)
    BDD_e  = build_BenDanielDuke_mx(m_e, Nz, dz, kz, period_SL)
    H_e  = np.diag(Ec) + BDD_e + np.diag(diag_e_kxy)

    # trous lourds
    diag_hh_kxy = (hbar**2 * (kx**2 + ky**2)) / (2.0*m_hh)
    BDD_hh = build_BenDanielDuke_mx(m_hh, Nz, dz, kz, period_SL)
    H_hh = np.diag(Ev) - BDD_hh - np.diag(diag_hh_kxy)

    # trous légers
    diag_lh_kxy = (hbar**2 * (kx**2 + ky**2)) / (2.0*m_lh)
    BDD_lh = build_BenDanielDuke_mx(m_lh, Nz, dz, kz, period_SL)
    H_lh = np.diag(Elh) - BDD_lh - np.diag(diag_lh_kxy)

    # so
    diag_so_kxy = (hbar**2 * (kx**2 + ky**2)) / (2.0*m_so)
    BDD_so = build_BenDanielDuke_mx(m_so, Nz, dz, kz, period_SL)
    H_so = np.diag(Eso) - BDD_so - np.diag(diag_so_kxy)

    ###########

    # dérivée avec conditions aux limites périodiques
    #D1 = Diff(0, dz, periodic=True) #pas utilisable avec pyodide
    D1 = first_derivative(Nz=Nz, dz=dz, kz=kz, period=period_SL)

    # P(z) * d/dz
    P_D1 = P_diag.dot(D1)  

    ###########
    
    # couplages e-/hh et e-/lh
    k_plus  = kx + 1j*ky
    k_minus = kx - 1j*ky

    H_E_HH = (-1j/np.sqrt(2)) * np.diag(P_array * k_minus)
    H_E_LH = (-1j/np.sqrt(6)) * np.diag(P_array * k_plus)

    H_E_SO = (-1j/np.sqrt(3)) * P_D1

    # conjoints
    H_HH_E = H_E_HH.conj().T
    H_LH_E = H_E_LH.conj().T
    H_SO_E = H_E_SO.conj().T

    # dimension 4Nz x 4Nz
    H1 = [H_e,      H_E_HH,     H_E_LH,     H_E_SO]
    H2 = [H_HH_E,   H_hh,       zeros,      zeros ]
    H3 = [H_LH_E,   zeros,      H_lh,       zeros ]
    H4 = [H_SO_E,   zeros,      zeros,      zeros ]

    # https://stackoverflow.com/questions/31469692/better-way-to-create-block-matrices-out-of-individual-blocks-in-numpy
    H = np.block([H1, H2, H3, H4])

    return H, Nz, dz
    


def compute_bands(kx, ky, kz, params):
    H, Nz, dz = build_kp4_hamiltonian(kx, ky, kz, params)

    # valeurs propres (J) et vecteurs propres
    E, psi = eigh(H)
    energies_eV = np.real(E) / q

    projs, labels = compute_projections_and_labels(E, psi, Nz, params)

    # collecte des énergies par label
    band_points = {0: [], 1: [], 2: [], 3: [], -1: []}
    for i in range(len(E)):
        band_points[labels[i]].append(energies_eV[i])

    E_e = np.array(sorted(band_points[0]))[::-1] if len(band_points[0])>0 else np.array([])
    E_hh = np.array(sorted(band_points[1]))[::-1] if len(band_points[1])>0 else np.array([])
    E_lh = np.array(sorted(band_points[2]))[::-1] if len(band_points[2])>0 else np.array([])
    E_so = np.array(sorted(band_points[3]))[::-1] if len(band_points[3])>0 else np.array([])

    return E_e, E_hh, E_lh, E_so, Nz, dz



def start_k_sweep(params, sweepType, k_range):
    e_e, e_hh, e_lh, e_so = [], [], [], []

    # sweep for k_z values
    if sweepType == "z":
        for _kz in k_range:
            E_e, E_hh, E_lh, E_so, Nz, dz = compute_bands(kx=0.0, ky=0.0, kz=_kz, params=params)
            e_e.append(E_e)
            e_hh.append(E_hh)
            e_lh.append(E_lh)
            e_so.append(E_so)

    # sweep for k_xy values
    if sweepType == "xy":
        for _kxy in k_range:
            E_e, E_hh, E_lh, E_so, Nz, dz = compute_bands(kx=_kxy, ky=0.0, kz=0.0, params=params)
            e_e.append(E_e)
            e_hh.append(E_hh)
            e_lh.append(E_lh)
            e_so.append(E_so)

    return {'E_e': e_e, 'E_hh': e_hh, 'E_lh': e_lh, 'E_so': e_so}