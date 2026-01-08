/**
 * interfaceManager.js
 */

class InterfaceManager {

    // Masque l'overlay une fois les modules chargés
    mask_overlay(overlay) {
        overlay = document.getElementById("loading-overlay");
        if (overlay) overlay.style.display = "none";
    }

    // Fermer tous les autres dropdowns
    // https://stackoverflow.com/questions/79617240/jquery-multi-select-dropdown-with-checkbox
    close_all_selects(current) {
        document.querySelectorAll(".multiselect").forEach(multiselect => {
          if (multiselect !== current) {
            multiselect.querySelector(".checkboxes").style.display = "none";
          }
        });
    }


    // Fermer si clic ailleurs
    close_when_outside() {
        document.addEventListener("click", () => {
          document.querySelectorAll(".checkboxes").forEach(box => {
            box.style.display = "none";
          });
        });
    }


    async handle_multiselect() {
        document.querySelectorAll(".multiselect").forEach(multiselect => {
          const selectBox = multiselect.querySelector(".selectBox");
          const checkboxes = multiselect.querySelector(".checkboxes");
          const radios = checkboxes.querySelectorAll("input[type=radio]");
          const selectedSpan = selectBox.querySelector("span");
          const xInput = multiselect.querySelector("input[type=number]");

          // état initial (au chargement)
          if (xInput) xInput.disabled = true;

          selectBox.addEventListener("click", (e) => {
            e.stopPropagation();
            this.close_all_selects(multiselect);
            checkboxes.style.display =
              checkboxes.style.display === "block" ? "none" : "block";
          });

          radios.forEach(radio => {
            radio.addEventListener("change", () => {
              selectedSpan.textContent = radio.value;
              checkboxes.style.display = "none";

              if (xInput) {
                const needsX = radio.value.includes("(x)");
                xInput.disabled = !needsX;
                if (!needsX) xInput.value = "0.0";
              }
            });
          });
        });
    
        this.close_when_outside();
    }


    // bloquages/debloquages si checkbox CSV activée
    handle_csv_blocks() {
      const customCheckbox = document.getElementById("customLinescan");

      // bloquages si checkbox CSV désactivé
      const csvBlock = document.getElementById("csvBlock");
      const buttonCompoBlock = document.getElementById("buttonCompoBlock");

      // bloquages si checkbox CSV activée !
      const inasBlock = document.getElementById("th_layer1");
      const inassbBlock = document.getElementById("th_layer2");

      const csvInput = document.getElementById("csvfile");

      // Au chargement : synchroniser l’état
      csvBlock.classList.toggle("disabled", !customCheckbox.checked);
      buttonCompoBlock.classList.toggle("disabled", !customCheckbox.checked);

      inasBlock.classList.toggle("enabled", !customCheckbox.checked);
      inassbBlock.classList.toggle("enabled", !customCheckbox.checked);

      csvInput.disabled = !customCheckbox.checked;

      customCheckbox.addEventListener("change", () => {
        const enabled = customCheckbox.checked;
        csvBlock.classList.toggle("disabled", !enabled);
        buttonCompoBlock.classList.toggle("disabled", !enabled);

        inasBlock.classList.toggle("disabled", enabled);
        inassbBlock.classList.toggle("disabled", enabled);

        csvInput.disabled = !enabled;
      });
    }
}

export default InterfaceManager;