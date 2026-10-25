# Provare l'app senza fare danni

Lezioni pagate care su MultiSession.

## Dati

- **Mai scrivere dati di prova nella cartella dati vera** (`%APPDATA%\<NomeApp>`): Danilo può
  averla già usata. Una volta ho sovrascritto `accounts.json` con dati di test e il suo account
  è andato ricostruito a mano. Avvia l'app con un profilo isolato:
  ```bash
  NOMEAPP_USER_DATA="<scratchpad>/test-profile" ./node_modules/electron/dist/electron.exe . --remote-debugging-port=9333
  ```
  (serve l'override `app.setPath('userData', …)` descritto in `finestra.md`).
- Prima di qualsiasi cosa che tocchi i dati veri (migrazioni, installazioni) copia i JSON in
  un backup.

## Processi

- Chiudi l'istanza di test filtrando per riga di comando, mai con `taskkill /IM electron.exe`
  (chiuderebbe anche le altre app Electron e l'istanza di Danilo):
  ```powershell
  Get-CimInstance Win32_Process -Filter "Name='electron.exe'" | Where-Object { $_.CommandLine -like '*remote-debugging-port=9333*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
  ```
- La finestra di test compare davanti a Danilo: tienila breve, e se la minimizza è normale.

## Guardare l'interfaccia

- `--remote-debugging-port` + Chrome DevTools Protocol (`http://127.0.0.1:9333/json`, poi
  `Runtime.evaluate` sulla pagina) per leggere il DOM e simulare azioni.
  Per aprire un menu Radix serve un `pointerdown` (non `click`); per scrivere in un input React
  usa il setter nativo di `value` + evento `input`.
- Gli screenshot di CDP (`Page.captureScreenshot`) **non sono affidabili** con `<webview>`
  impilate: possono mostrare vuoto ciò che a schermo c'è. Per vedere la finestra vera usa
  `PrintWindow` di Win32 (con flag 2) sull'handle della finestra principale, poi leggi il PNG.
- Le finestre minimizzate (coordinate -32000) non vengono disegnate: ripristinale con
  `ShowWindow(h, 9)` prima di catturarle.

## Verifica

- `npm run typecheck` e `npm run build` puliti prima di provare.
- Prova ogni modifica davvero, non solo che compili: avvio, l'azione, chiusura e riavvio
  (lo stato torna?), tema chiaro e scuro.
- Se Danilo dice di far verificare a un'altra sessione, non verificare tu: mandale cosa è
  cambiato e cosa controllare, e lascia che riferisca a lui.
