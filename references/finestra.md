# Finestra: barra del titolo integrata

Niente barra del titolo del sistema: la barra in alto dell'app (schede, titolo, azioni) fa da
barra del titolo, con i pulsanti nativi di Windows (minimizza/ingrandisci/chiudi, snap layout
compreso) disegnati sopra nei colori del tema.

## Main process

```ts
import { BrowserWindow, type TitleBarOverlayOptions } from 'electron'

// Stessa altezza e stessi toni della barra in alto (--color-chrome / --color-foreground).
const TITLE_BAR_HEIGHT = 48
const titleBarOverlay = (theme: 'light' | 'dark'): TitleBarOverlayOptions =>
  theme === 'dark'
    ? { color: '#1e1e1c', symbolColor: '#ebe8e0', height: TITLE_BAR_HEIGHT }
    : { color: '#f1efe8', symbolColor: '#2b2a27', height: TITLE_BAR_HEIGHT }

const win = new BrowserWindow({
  // ...bounds da window-state
  minWidth: 640,
  minHeight: 420,
  show: false,
  backgroundColor: theme === 'dark' ? '#262624' : '#FAF9F5', // niente lampo bianco all'avvio
  autoHideMenuBar: true,
  icon: isDev ? join(__dirname, '../../build/icon.png') : undefined, // nel pacchetto la prende dall'exe
  ...(process.platform === 'darwin'
    ? { titleBarStyle: 'hiddenInset' as const }
    : { titleBarStyle: 'hidden' as const, titleBarOverlay: titleBarOverlay(theme) }),
  webPreferences: {
    preload: join(__dirname, '../preload/index.js'),
    contextIsolation: true,
    nodeIntegration: false,
    sandbox: true
  }
})
win.once('ready-to-show', () => win.show())
```

Quando il tema cambia (il renderer lo salva via IPC), aggiorna i pulsanti:
`win.setTitleBarOverlay(titleBarOverlay(nuovoTema))` (non su macOS).

Su Windows/Linux togli il menu: `Menu.setApplicationMenu(null)` (su macOS tienilo, serve per
copia/incolla).

## Renderer

La barra in alto riceve la classe `titlebar` e lascia spazio ai pulsanti nativi:

```tsx
<div
  className={cn('titlebar flex h-12 shrink-0 items-center gap-2 bg-chrome pr-2',
    window.api.platform === 'darwin' ? 'pl-20' : 'pl-3')}
  // Window Controls Overlay: spazio per i pulsanti nativi a destra
  style={{ paddingRight: 'calc(100vw - env(titlebar-area-x, 0px) - env(titlebar-area-width, 100vw) + 8px)' }}
>
```

`window.api.platform` arriva dal preload (`platform: process.platform` nell'oggetto esposto con
`contextBridge`). Su macOS `pl-20` lascia posto ai tre pallini.

CSS (già in `assets/globals.css`): lo spazio vuoto trascina la finestra (doppio click la
ingrandisce), tutto ciò che è cliccabile resta interattivo.

```css
@layer components {
  .titlebar { -webkit-app-region: drag; }
  .titlebar :is(button, [role="tab"], a, input) { -webkit-app-region: no-drag; }
}
```

Se metti nella barra un elemento cliccabile che non è `button`/`a`/`input`/`[role=tab]`,
dagli `[-webkit-app-region:no-drag]` o non riceverà i click.

## Altro che ogni app dovrebbe avere

- **Una sola istanza** (`app.requestSingleInstanceLock()`, al secondo avvio porta in primo piano
  la finestra esistente): due istanze si sovrascriverebbero i file di stato.
- **Posizione e dimensione salvate**: `assets/electron/window-state.ts` (debounce su
  resize/move, `getNormalBounds()`, scarta la posizione se il monitor non c'è più). Chiama
  `trackWindowState(win)` e salva anche su `close`.
- **Stato su file JSON in `userData`** con scrittura atomica (tmp + rename) e autosave
  debounced, non solo su `close` (un crash o un kill non lo fa scattare): vedi
  `assets/electron/storage.reference.ts`.
- **Sicurezza**: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`, il
  renderer parla col main solo tramite l'API esposta dal preload. La pagina host non deve
  navigare (`will-navigate` → `preventDefault`) né aprire finestre (`setWindowOpenHandler` → deny).
- **Override per i test**: `if (process.env.NOMEAPP_USER_DATA) app.setPath('userData', ...)`
  prima del single-instance lock, così i test non toccano i dati veri.

Solo per app che mostrano siti esterni (webview):
- `app.userAgentFallback` con uno user agent Chrome reale (molti siti bloccano "Electron").
- `app.commandLine.appendSwitch('disable-features', 'CalculateNativeWinOcclusion')` e
  `backgroundThrottling: false` se le pagine devono continuare a lavorare con la finestra
  coperta da altre app.
