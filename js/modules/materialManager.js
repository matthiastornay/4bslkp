/**
 * materialManager.js
 */

class MaterialManager {
    
    // vérifie si un fichier CSV a été selectionné
    check_csv(file) {
        if (!file) {
            console.log("Aucun fichier de composition sélectionné !");
            alert("Merci de choisir un fichier de composition CSV avant de tracer !");
            return false;
        }
        return true
    }


    // récupérer la valeur choisie pour chaque layer
    get_layer_material(layerId) {
        const layer = document.getElementById(layerId);
        const checked = layer.querySelector("input[type=radio]:checked");
        return checked ? checked.value : document.getElementById(layerId+"Span");
    }


    get_param_value(id, parser="float") {
        if (document.getElementById(id)){
            if (parser=="float") return parseFloat(document.getElementById(id).value);
            if (parser=="int") return parseInt(document.getElementById(id).value, 10);
        } 
        // sinon, null
        return null;
    }


    read_checkbox(id) {

        const isChecked = document.getElementById(id).checked;
        const python_bool = isChecked ? "True" : "False"; // pour Python

        return python_bool;
    }


    read_user_inputs() {

        const params = {
            th_layer1: this.get_param_value("th_layer1"),
            th_layer2: this.get_param_value("th_layer2"),
            Vc: this.get_param_value("Vc"),
            Vh: this.get_param_value("Vh"),
            Gamma_bow_1: this.get_param_value("Gamma_bow_1"),
            Gamma_bow_2: this.get_param_value("Gamma_bow_2"),
            Vb_bow_1: this.get_param_value("Vb_bow_1"),
            Vb_bow_2: this.get_param_value("Vb_bow_2"),
            D_SO_1: this.get_param_value("D_SO_1"),
            D_SO_2: this.get_param_value("D_SO_2"),
            dz: this.get_param_value("dz"),
            Ep_1: this.get_param_value("Ep_1"),
            Ep_2: this.get_param_value("Ep_2"),
            nk: this.get_param_value("nk", "int"),
            temperature: this.get_param_value("temperature"),

            me_1: this.get_param_value("me_1"),
            me_2: this.get_param_value("me_2"),
            mhh_1: this.get_param_value("mhh_1"),
            mhh_2: this.get_param_value("mhh_2"),
            mlh_1: this.get_param_value("mlh_1"),
            mlh_2: this.get_param_value("mlh_2"),
            mso_1: this.get_param_value("mso_1"),
            mso_2: this.get_param_value("mso_2"),

            mat_layer1: this.get_layer_material("layer1Select"),
            mat_layer2: this.get_layer_material("layer2Select"),
            x_layer1: this.get_param_value("compoL1"),
            x_layer2: this.get_param_value("compoL2"),
            delta_strain_layer1: this.get_param_value("strain_layer1"),
            delta_strain_layer2: this.get_param_value("strain_layer2"),

            flag_E_plot: this.read_checkbox("E_plot"),
            flag_HH_plot: this.read_checkbox("HH_plot"),
            flag_LH_plot: this.read_checkbox("LH_plot"),
            flag_SO_plot: this.read_checkbox("SO_plot"),

            linescan_bool: this.read_checkbox("customLinescan"),

            Emin_plot: this.get_param_value("Emin"),
            Emax_plot: this.get_param_value("Emax"),
        }

        return params;
    }


    parse_user_inputs(button_name) {

        if (button_name == "plotHeterostructure" || button_name == "calculateDispersion" || button_name == "loadDatabase") {
            
            const user_inputs = this.read_user_inputs();
            return user_inputs;

        }
    }
}

export default MaterialManager;