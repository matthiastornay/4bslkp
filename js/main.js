/**
 * main.js
 */


// lève une erreur et renvoie -1 si erreur sur les inputs materials, sinon renvoie 0
function check_user_materials() {
    if ( document.getElementById("layer1SelectSpan").textContent == "Material" && inputs_dict.linescan_bool ) {
        alert("Erreur sur la sélection des matériaux.");
        return -1;
    }

    if ( document.getElementById("layer1SelectSpan").textContent == "Material" && document.getElementById("layer2SelectSpan").textContent == "Material" ) {
        alert("Erreur sur la sélection des matériaux.");
        return -1;
    }

    return 0; // renvoie 0 si pas d'erreur d'input material
}



async function plotCompositions() {
  const pyodideInst = await pyodideReadyPromise;

  document.getElementById("figures").innerHTML = "";
  document.getElementById("output").innerHTML = "";

  
  const isLinescan = document.getElementById("customLinescan").checked;
  const linescan_bool = isLinescan ? "True" : "False";

  const fileInput = document.getElementById("csvfile");
  const file = fileInput.files[0];

  // vérifie la présence d'un fichier CSV
  if (!matManager.check_csv(file)) return
  
  if (file && linescan_bool) {
    const csvText = await file.text();
    pyodide.globals.set("csv_text", csvText);
  }

  try {
    const pyResult = await pyodideInst.runPythonAsync(`
      import io
      import pandas as pd

      df = pd.read_csv(io.StringIO(csv_text))

      plot_custom_compo(__linescan=${linescan_bool}, __df_CSV_file=df)
    `);

  } catch (err) {
    console.error(err);
  }
}



async function loadDatabase() {

  const inputs_dict = matManager.parse_user_inputs("loadDatabase");
  pyManager.setGlobal('inputs_dict', inputs_dict);

  if (check_user_materials() == -1) return;

  try {
    const pyResult = await pyManager.execAsyncPython(`
      import io
      import pandas as pd

      inputs = inputs_dict
      inputs = inputs.to_py()

      if inputs['linescan_bool'] == "False": inputs['linescan_bool'] = False
      if inputs['linescan_bool'] == "True": inputs['linescan_bool'] = True

      if inputs['linescan_bool']:
        df = pd.read_csv(io.StringIO(csv_text))
      else:
        df = None

      __heterostructure_bool = False

      res = kp4(js_input=inputs, __df_CSV_file=df, __heterostructure_bool=__heterostructure_bool, action="loadDatabase")
    
      res
    `);

    
  const [Gbow1, Gbow2, Vbow1, Vbow2, Dso1, Dso2, Ep1, Ep2, me1, me2, mhh1, mhh2, mlh1, mlh2, mso1, mso2] = pyResult;
    
  document.getElementById("Gamma_bow_1").value = Gbow1.toFixed(2);
  document.getElementById("Gamma_bow_2").value = Gbow2.toFixed(2);
  document.getElementById("Vb_bow_1").value = Vbow1.toFixed(2);
  document.getElementById("Vb_bow_2").value = Vbow2.toFixed(2);
  document.getElementById("D_SO_1").value = Dso1.toFixed(3);
  document.getElementById("D_SO_2").value = Dso2.toFixed(3)
  document.getElementById("Ep_1").value = Ep1.toFixed(2);
  document.getElementById("Ep_2").value = Ep2.toFixed(2);
  document.getElementById("me_1").value = me1.toFixed(3);
  document.getElementById("me_2").value = me2.toFixed(3);
  document.getElementById("mhh_1").value = mhh1.toFixed(3);
  document.getElementById("mhh_2").value = mhh2.toFixed(3);
  document.getElementById("mlh_1").value = mlh1.toFixed(3);
  document.getElementById("mlh_2").value = mlh2.toFixed(3);
  document.getElementById("mso_1").value = mso1.toFixed(3);
  document.getElementById("mso_2").value = mso2.toFixed(3);


  } catch (err) {
    console.error(err);
  }

}



async function plotHeterostructure() {

  const inputs_dict = matManager.parse_user_inputs("plotHeterostructure");
  pyManager.setGlobal('inputs_dict', inputs_dict);

  // attention, on récupère bien l'ID, car au reload d'une page le matériau peut
  // toujours être sélectionné et récupéré dans le cache, mais ça ne met pas forcément
  // à jour la valeur du multiselect. Là, on s'assure que l'utilisateur fasse un choix explicite.

  if (check_user_materials() == -1) return;

  document.getElementById("figures").innerHTML = "";
  document.getElementById("output").innerHTML = "";

  // mise à jour spinner
  statusElement_H.style.display = "block";
  if (runBtn_H) runBtn_H.disabled = true;

  await new Promise(requestAnimationFrame);


  const fileInput = document.getElementById("csvfile");
  const file = fileInput.files[0];

  if (inputs_dict.linescan_bool == "True" && !file){
    alert("Merci de charger un fichier CSV.");
    return;
  }

  if (!file) {
    console.log("Aucun fichier sélectionné. On utilise les données abruptes.");
    //alert("Merci de choisir un fichier CSV avant de tracer !");
    //return;
  } else if (file && inputs_dict.linescan_bool) {
    const csvText = await file.text();
    pyManager.setGlobal("csv_text", csvText);
  }

  try {


    const pyResult = pyManager.execAsyncPython(`
      import io
      import pandas as pd

      inputs = inputs_dict
      inputs = inputs.to_py()

      if inputs['linescan_bool'] == "False": inputs['linescan_bool'] = False
      if inputs['linescan_bool'] == "True": inputs['linescan_bool'] = True

      if inputs['linescan_bool']:
        df = pd.read_csv(io.StringIO(csv_text))
      else:
        df = None

      __heterostructure_bool = True

      res = kp4(js_input=inputs, __df_CSV_file=df, __heterostructure_bool=__heterostructure_bool)
    
      res
    `);

  } catch (err) {
    //writeLog("Erreur : " + err);
    console.error(err);
  } finally {
    statusElement_H.style.display = "none";
    if (runBtn_H) runBtn_H.disabled = false;
  }
}



async function calculateDispersion() {

  document.getElementById("figures").innerHTML = "";
  document.getElementById("output").innerHTML = "";

  document.getElementById("output").textContent = "";

  // mise à jour spinner
  statusElement_D.style.display = "block";
  if (runBtn_D) runBtn_D.disabled = true;

  await new Promise(requestAnimationFrame);

  const inputs_dict = matManager.parse_user_inputs("calculateDispersion");
  pyManager.setGlobal('inputs_dict', inputs_dict);

  const fileInput = document.getElementById("csvfile");
  const file = fileInput.files[0];

  if (!file) {
    console.log("Aucun fichier sélectionné. On utilise les données abruptes.");
    //alert("Merci de choisir un fichier CSV avant de tracer !");
    //return;
  } else {

    if (file && inputs_dict.linescan_bool) {
      const csvText = await file.text();
      pyManager.setGlobal("csv_text", csvText);
    }

  }


  try {

    // ATTENTION : await ici (on attend la promise)
    const pyResult = await pyManager.execAsyncPython(`
      import io
      import pandas as pd

      inputs = inputs_dict
      inputs = inputs.to_py()

      if inputs['linescan_bool'] == "False": inputs['linescan_bool'] = False
      if inputs['linescan_bool'] == "True": inputs['linescan_bool'] = True

      if inputs['linescan_bool']:
        df = pd.read_csv(io.StringIO(csv_text))
      else:
        df = None

      __heterostructure_bool = False

      # On envoie finalement un df à la fonction
      res = kp4(js_input=inputs, __df_CSV_file=df, __heterostructure_bool=__heterostructure_bool)

      res
    `);
    
    const [meff_hh_z, meff_lh_z, meff_e_z, meff_hh_xy, meff_lh_xy, meff_e_xy, Egap, delta] = pyResult;
        
    document.getElementById("output").textContent = `
      m*_e_Z = ${meff_e_z} m0     m*_hh_XY = ${meff_e_xy} m0
      m*_hh_Z = ${meff_hh_z} m0     m*_hh_XY = ${meff_hh_xy} m0
      m*_lh_Z = ${meff_lh_z} m0     m*_hh_XY = ${meff_lh_xy} m0
      E_gap = ${Egap} meV
      δ_HH/LH = ${delta} meV
    `;

  
  } catch (err) {
    console.error(err);
  } finally {
    statusElement_D.style.display = "none";
    if (runBtn_D) runBtn_D.disabled = false;
  }
}


/* ############################################################################################# */

import PyodideManager from './modules/pyodideManager.js';
import InterfaceManager from './modules/interfaceManager.js';
import MaterialManager from './modules/materialManager.js';

const pyManager = new PyodideManager();
const uiManager = new InterfaceManager();
const matManager = new MaterialManager();

// initialisation de pyodide
await pyManager.initialize();

// démasquage de l'overlay
uiManager.mask_overlay();

// gestion event boutons
document.getElementById("Btn_loadDatabase").addEventListener("click", loadDatabase);
document.getElementById("Btn_plotCompositions").addEventListener("click", plotCompositions);
document.getElementById("Btn_plotHeterostructure").addEventListener("click", plotHeterostructure);
document.getElementById("Btn_calculateDispersion").addEventListener("click", calculateDispersion);

// gestion de l'apparition des spinners
const statusElement_H = document.getElementById("status_H");
const statusElement_D = document.getElementById("status_D");
const runBtn_H = document.getElementById("runBtn_H"); // maintenant non null
const runBtn_D = document.getElementById("runBtn_D"); // maintenant non null

// gestion du choix des matériaux
uiManager.handle_multiselect();

// bloquages/debloquages si checkbox CSV activée
uiManager.handle_csv_blocks()

