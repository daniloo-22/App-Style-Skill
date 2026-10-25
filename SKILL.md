---
name: app-desktop-stile
description: Crea o ristruttura un'app desktop di Danilo con lo stesso stile, la stessa finestra, la stessa icona e la stessa installazione di MultiSession - palette calda crema/terracotta in token Tailwind v4, componenti shadcn già adattati, tema chiaro/scuro, barra del titolo integrata con i pulsanti nativi di Windows, icona generata da prompt e convertita in PNG/ICO, installer electron-builder one-click con collegamenti su desktop e Start. Usala quando Danilo chiede di fare una nuova app desktop, di applicare "lo stesso stile" o "lo stile di MultiSession" a un'altra app, di farle l'icona, di installarla "come un'app vera" o di aggiornarla, anche se nomina solo una di queste cose.
---

# App desktop nello stile di MultiSession

Rispondi in italiano. Il riferimento vivo è `C:\Users\Danil\Desktop\DanMultiSession`: se un
dettaglio non è qui, guarda come è fatto lì prima di inventare.

## Cosa contiene

| Percorso | A cosa serve |
| --- | --- |
| `assets/globals.css` | Palette e token (`@theme`), tema scuro `.dark`, font, raggi, ombre, regola `.titlebar` |
| `assets/ui/*.tsx` | Componenti shadcn già allineati ai token: button, input, label, dialog, alert-dialog, dropdown-menu, tooltip, color-picker |
| `assets/utils.ts`, `assets/colors.ts` | `cn()` e le otto tinte smorzate per i colori scelti dall'utente |
| `assets/components.json` | Config shadcn (alias `@/components/ui`, `@/lib/utils`) |
| `assets/electron/` | `electron.vite.config.ts`, `window-state.ts`, `storage.reference.ts` (stato JSON atomico + autosave), `electron-builder.yml` |
| `references/stile.md` | Le regole visive e gli schemi ricorrenti (pill, stati vuoti, conferme, avvisi) |
| `references/finestra.md` | Barra del titolo integrata, istanza singola, stato finestra, sicurezza |
| `references/icona.md` | Prompt dell'icona e conversione |
| `references/installazione.md` | Installer one-click e procedura di aggiornamento |
| `references/test.md` | Come provare senza toccare i dati veri |
| `scripts/make_icon.py` | Immagine generata → `build/icon.png`, `icon.ico`, anteprima piccole taglie |
| `scripts/install-update.ps1` | Chiusura pulita, backup dati, installazione, riapertura |

Leggi i riferimenti della parte su cui stai lavorando, non tutti in blocco.

## Procedura

### 1. Capire l'app

- App nuova: stack di MultiSession, cioè electron-vite (main/preload/renderer in un progetto,
  HMR sul renderer), React + TypeScript, Tailwind v4 CSS-first, shadcn/ui, lucide-react,
  Zustand come store unico. Niente Next.js per un'app a finestra singola.
- App esistente: leggi prima `package.json`, la struttura e come gestisce gli stili. Adatta, non
  riscrivere: porta token e componenti dove servono, conserva la logica. Se non è Electron
  applica solo stile (2) e icona (4).

### 2. Stile

1. Copia `assets/globals.css` nel CSS globale del renderer (unico file) e importalo
   dall'entry. Con Vite aggiungi il plugin `@tailwindcss/vite`.
2. Copia i componenti di `assets/ui/` che servono in `src/components/ui/`, `utils.ts` e
   `colors.ts` in `src/lib/`, e installa le loro dipendenze (elenco in `references/stile.md`).
3. Sostituisci colori, ombre, raggi e font sparsi nel codice con i token. Nessun hex nei
   componenti, ombre solo su ciò che fluttua, accento solo su attivo/focus/primario.
4. Tema scuro: classe `dark` su `<html>`, preferenza salvata, pulsante sole/luna.

### 3. Finestra (solo Electron)

Segui `references/finestra.md`: `titleBarStyle: 'hidden'` + `titleBarOverlay` nei colori del
tema (aggiornati al cambio tema), barra in alto con classe `titlebar` e padding per i
pulsanti nativi, istanza singola, stato finestra salvato, stato app in JSON con autosave.

### 4. Icona

Scrivi il prompt dal modello in `references/icona.md`, adattando il concetto a cosa fa l'app,
e dallo a Danilo: l'immagine la genera lui. Quando la manda, convertila con
`scripts/make_icon.py` e controlla l'anteprima. Se dice di aspettare per l'icona, aspetta.

### 5. Installazione (solo Electron)

Segui `references/installazione.md`: `electron-builder.yml` dal modello, dipendenze del
renderer in `devDependencies`, `npm run dist:win`. Per installare o aggiornare usa
`scripts/install-update.ps1`, **dopo aver chiesto** se l'app è aperta.

### 6. Verifica

`npm run typecheck` e `npm run build`, poi prova davvero l'app con un profilo dati isolato
(`references/test.md`): avvio, le funzioni toccate, tema chiaro e scuro, chiusura e riavvio.
Guarda la finestra vera (PrintWindow), non solo il DOM.

## Da non fare

- Scrivere dati di prova in `%APPDATA%\<NomeApp>` o chiudere processi con
  `taskkill /IM electron.exe`.
- Aggiungere loghi, nomi o simboli di prodotti esistenti all'interfaccia o all'icona.
- Grigio-blu, nero puro, grassetti pesanti, ombre su card e barre, accento su grandi superfici.
- Installare o reinstallare senza chiedere, o chiudere l'app con un kill invece che con la X.
