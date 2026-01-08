/**
 * pyodideManager.js
 */

class PyodideManager {

  constructor() {
    this.pyodide = null;
    this.isReady = false;
    this.initPromise = null;
  }

  // Initialise pyodide
  async initialize() {
    if (this.initPromise) {
      return this.initPromise;
    }

    this.initPromise = this._doInitialize();
    return this.initPromise;
  }


  async _doInitialize() {
    try {
      this.pyodide = await loadPyodide();
      await this.pyodide.loadPackage(["numpy", "matplotlib", "scipy", "pandas", "micropip"]);

      await this._configure_Python2JS_redirection();

      // Installation de mpld3 via micropip
      await this.pyodide.runPythonAsync(`
        import micropip
        await micropip.install("mpld3")
      `);

      // Chargement des fichiers Python du projet
      await this._load_Python_files();

      this.isReady = true;
      console.log("Initialisation de Pyodide OK");
    } catch (error) {
      console.error("Erreur à l'initialisation de Pyodide:", error);
      throw error;
    }
  }


  // Redirige les print() en Python vers le JS pour affichager HTML
  async _configure_Python2JS_redirection() {
    await this.pyodide.runPythonAsync(`
      import sys

      class JSWriter:
          def write(self, s):
              import js
              if hasattr(js, 'writeLog'):
                  js.writeLog(s)
          def flush(self):
              pass
      
      sys.stdout = JSWriter()
      sys.stderr = JSWriter()
    `);
  }

  
  // Load les fichiers python du projet dans le path de pyodide
  async _load_Python_files() {
    const pythonFiles = [
      { path: "kp4.py", url: "kp4.py" },
      { path: "__init__.py", url: "__init__.py" },
      { path: "constants.py", url: "constants.py" },
      { path: "utils.py", url: "utils.py" },
      { path: "materials.py", url: "materials.py" },
      { path: "band_calculations.py", url: "band_calculations.py" },
    ];

    for (const file of pythonFiles) {
      try {
        const code = await fetch(file.url).then(r => r.text());
        
        // Créer l'arborescence au besoin
        const dir = file.path.substring(0, file.path.lastIndexOf("/"));
        if (dir) {
          try {
            this.pyodide.FS.mkdirTree(dir);
          } catch (e) {
            // Ok si le dossier existe déjà
          }
        }
        
        // Écrire le fichier dans le système de fichiers Pyodide
        this.pyodide.FS.writeFile(file.path, code);
      } catch (error) {
        console.error(`Erreur lors du chargement de ${file.path}:`, error);
        throw error;
      }
    }

    // Charge le module principal Python et attend qu'il soit exécuté
    const pyCode = await fetch("kp4.py").then(r => r.text());
    await this.pyodide.runPythonAsync(pyCode);
  }


  // exécute code Python et renvoie le résultat
  async execAsyncPython(code, toJS_flag=false) {
    if (!this.isReady) {
      throw new Error("Pyodide n'est pas encore initialisé");
    }

    try {     // ATTENTION : await ici (on attend la promise)
      const pyResult = await this.pyodide.runPythonAsync(code);

      if (toJS_flag) {
        const result = pyResult.toJs();
        pyResult.destroy();
        return result
      }

      return pyResult;
      
    } catch (error) {
      console.error("Erreur lors de l'exécution Python:", error);
      throw error;
    }
  }


  // définit une variable globale Python
  setGlobal(name, value) {
    if (!this.isReady) {
      throw new Error("Pyodide n'est pas encore initialisé");
    }
    this.pyodide.globals.set(name, value);
  }


  // récupère une variable globale Python
  getGlobal(name) {
    if (!this.isReady) {
      throw new Error("Pyodide n'est pas encore initialisé");
    }
    return this.pyodide.globals.get(name);
  }


  // Vérifie que tous les modules sont chargés et que pyodide est prêt
  get ready() {
    return this.isReady;
  }
}

// Export pour utilisation en module ES6
export default PyodideManager;