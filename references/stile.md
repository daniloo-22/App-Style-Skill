# Linguaggio visivo

Palette calda e desaturata, niente grigio-blu da "app Electron". Tutti i valori stanno in
`assets/globals.css`: è l'unica fonte, da copiare così com'è e ritoccare solo lì.

## Regole

- **Sfondo** crema molto chiaro `#FAF9F5`; superfici (dialog, input, card) appena più chiare
  `#FDFCFA`; testo nero caldo `#2B2A27`, mai nero puro. Testo secondario `#78756D`.
- **Un solo accento**, terracotta spento `#B9694E`, usato con parsimonia: elemento attivo
  (scheda, voce selezionata), focus ring, pulsante primario. Mai per riempire grandi aree.
- **Separazione con bordi sottili** a basso contrasto (`#E5E2D9`), non con ombre. Ombra
  quasi impercettibile (`shadow-float`) solo su ciò che fluttua davvero: dialog, menu, avvisi.
- **Raggi**: 10px contenitori (`rounded-lg`), 8px input e bottoni (`rounded-md`), pill
  completamente arrotondate (`rounded-full`) per schede, chip, selettori e campo URL/ricerca.
- **Spaziatura ampia**, densità bassa: dialog con `p-7` e `gap-6`, righe di lista `py-2`,
  barre alte 48px (`h-12`). Meglio un po' di respiro in più che una UI compressa.
- **Tipografia** di sistema: `ui-sans-serif, -apple-system, "Segoe UI Variable Text", "Segoe UI",
  Inter`. Peso 500 (`font-medium`) per label, titoli e voce attiva; 400 per il resto. Niente
  grassetti pesanti. Su Windows serve "Segoe UI Variable Text": il Segoe UI classico non ha il 500
  e lo rende semibold. Corpo 14px, 13px nelle barre.
- **Hover e active** appena percettibili: `bg-hover` (nero caldo al 4,5%) e `bg-active` (8%).
  Transizioni 120-150ms (`--default-transition-duration: 140ms`), solo su colore e sfondo.
- **Barre (titolo/schede e strumenti)** senza bordi marcati: si distinguono dall'area contenuto
  solo per una minima differenza di tono (`bg-chrome` `#F1EFE8`, `bg-toolbar` `#F5F4EE`).
- **Tema scuro** con la stessa logica: grigio caldo `#262624` (non nero), superfici `#2D2C29`,
  accento schiarito `#CC7D61`. Strategia `class` di Tailwind (`.dark` su `<html>`), preferenza
  salvata e commutabile da un pulsante sole/luna.
- **Nessun logo, nome o marchio di prodotti esistenti** nell'interfaccia.

## Tailwind v4

- Configurazione CSS-first: `@import "tailwindcss"`, `@custom-variant dark`, token in `@theme`.
  Niente `tailwind.config.js`. Plugin Vite `@tailwindcss/vite`.
- `@theme` azzera la palette di default (`--color-*: initial`): si usano solo i token del
  progetto (`bg-background`, `bg-surface`, `text-muted-foreground`, `border-border`,
  `bg-accent`, `ring-ring`, `bg-hover`, `bg-active`, `bg-overlay`, `text-destructive`…).
  Se serve un colore nuovo, aggiungilo come token in entrambi i temi, mai un hex nel componente.
- I colori "dati" (pallini degli account, colori scelti dall'utente) vengono da `assets/colors.ts`:
  otto tinte smorzate e calde che stanno bene accanto all'accento.

## Componenti (shadcn/ui, già adattati)

In `assets/ui/` ci sono le versioni già allineate ai token: `button`, `input`, `label`,
`dialog`, `alert-dialog`, `dropdown-menu`, `tooltip`, più `color-picker`. Installa solo i
pacchetti Radix che servono (`@radix-ui/react-dialog`, `-alert-dialog`, `-dropdown-menu`,
`-tooltip`, `-label`, `-slot`), più `class-variance-authority`, `clsx`, `tailwind-merge`,
`lucide-react`. `components.json` è pronto se vuoi aggiungerne altri con la CLI shadcn: dopo
averli aggiunti, sostituisci i colori di default con i token qui sopra.

Varianti di `Button`: `default` (accento, solo azione primaria), `outline`, `ghost`, `subtle`
(icone nelle barre: testo secondario che si scurisce all'hover), `destructive`.

## Schemi ricorrenti

- **Icone** `lucide-react`, 16px (`size-4`), colore `text-muted-foreground` negli elenchi.
- **Pill attiva**: `bg-surface` + `ring-1 ring-accent/45` + `font-medium`; inattiva trasparente
  con `hover:bg-hover`.
- **Stato vuoto**: icona in un cerchio `bg-hover` da 48px, titolo `text-base font-medium`,
  una riga di spiegazione `text-muted-foreground`, poi l'azione.
- **Errori leggibili**: messaggio umano in italiano + dettaglio tecnico piccolo e attenuato +
  pulsante "Riprova" `outline`.
- **Conferme distruttive**: `AlertDialog` con titolo a domanda ("Eliminare “X”?"), cosa
  succede e se è annullabile, pulsante `destructive` con il verbo ("Elimina", "Svuota").
- **Avvisi temporanei** in basso a destra: card `bg-surface` con bordo e `shadow-float`,
  6 secondi, massimo tre impilati.
- **Tooltip** su ogni pulsante solo icona; sui dialog con pulsanti icona in alto usa
  `onOpenAutoFocus={(e) => e.preventDefault()}`, altrimenti il focus apre subito un tooltip.
- **Testi** in italiano, tono diretto, senza punti esclamativi.
