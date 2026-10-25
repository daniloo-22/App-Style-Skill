# Installazione come un'app vera

Obiettivo: l'app si apre come qualsiasi programma (collegamento sul desktop e nel menu Start),
non con `npm run dev`.

## Setup

- `electron-builder` come devDependency, config in `electron-builder.yml` (modello in
  `assets/electron/electron-builder.yml`: sostituisci `NOMEAPP`/`NomeApp`).
- NSIS **one-click per utente**: installa in `%LOCALAPPDATA%\Programs\<NomeApp>`, nessun
  prompt da amministratore, collegamenti su desktop e Start, `deleteAppDataOnUninstall: false`
  (disinstallare non cancella i dati dell'utente).
- `package.json`: `productName` = nome visibile (decide anche la cartella `%APPDATA%\<NomeApp>`),
  `main: ./out/main/index.js`, script:
  ```json
  "build": "electron-vite build",
  "dist": "npm run build && electron-builder",
  "dist:win": "npm run build && electron-builder --win"
  ```
- **Tutte le dipendenze del renderer in `devDependencies`**: Vite le ha già messe nel bundle,
  e se restano in `dependencies` electron-builder le ricopia nell'installer. Il main di solito
  usa solo `electron` e moduli Node; se usa un pacchetto vero, quello resta in `dependencies`.
- Icona in `build/` (vedi `icona.md`).
- Il primo `npm run dist:win` scarica NSIS e 7zip: è normale che ci metta qualche minuto.

## Installare o aggiornare

Rigenera con `npm run dist:win` (output `dist\<NomeApp> Setup <versione>.exe`), poi usa lo
script, che fa tutto nell'ordine giusto:

```bash
powershell -ExecutionPolicy Bypass -File "C:/Users/Danil/.claude/skills/app-desktop-stile/scripts/install-update.ps1" -AppName NomeApp -Installer "<progetto>\dist\NomeApp Setup 1.0.0.exe"
```

1. chiude l'app come la X (`CloseMainWindow`, così salva lo stato), mai un kill forzato;
2. copia i JSON di stato da `%APPDATA%\<NomeApp>` in una cartella `backup-<data>`;
3. lancia l'installer e aspetta che finisca;
4. riapre l'app dal collegamento sul desktop (`runAfterFinish` non sempre scatta quando
   l'installer viene lanciato da script).

Regole:
- **Chiedi prima di installare o aggiornare** se l'app è aperta: chiuderla interrompe il lavoro
  di Danilo (o di un'altra sessione Claude che la sta usando). L'ok vale per quella volta.
- Dopo l'installazione verifica che il pacchetto contenga davvero la modifica, per esempio
  cercando una stringa nuova in `resources\app.asar` con `Select-String -SimpleMatch`.
- I dati in `%APPDATA%\<NomeApp>` restano tra un'installazione e l'altra. Se la nuova versione
  cambia il formato dei file, scrivi la migrazione nel main (vecchio formato → nuovo al
  caricamento) e fai il backup prima.
- L'installer non è firmato: al primo avvio Windows SmartScreen mostra "PC protetto" →
  "Ulteriori informazioni" → "Esegui comunque". Dillo a Danilo la prima volta.
- Se l'app espone un server MCP, dopo l'installazione registralo puntando al file installato
  (`%LOCALAPPDATA%\Programs\<NomeApp>\resources\...`), non alla cartella del progetto. Le
  sessioni Claude già aperte vedono i tool nuovi solo dopo un riavvio.

Vale anche per un'app esistente: se non è Electron (per esempio una web app), questa parte non
si applica; applica solo stile e icona.
