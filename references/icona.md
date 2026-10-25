# Icona

L'icona la genera Danilo con un generatore di immagini a partire da un prompt; tu scrivi il
prompt, poi converti l'immagine che ti passa. Non disegnare l'icona da solo e non generarla
con script se non te lo chiede.

## Stile (MultiSession come riferimento)

Riquadro arrotondato (squircle) crema `#FAF9F5` con un bordo sottilissimo `#E5E2D9`; al centro
2-3 forme piatte e morbide, leggermente organiche (come carta ritagliata), nei toni della
palette: terracotta `#B9694E` davanti, sabbia `#C49A4A` e grigio-bruno `#857A6C` dietro.
Niente gradienti, lucidi, 3D o testo. Deve leggersi a 16px.

## Prompt (modello)

Sostituisci CONCETTO con una metafora visiva semplice di cosa fa l'app (per MultiSession:
"tre pill a forma di scheda impilate e leggermente sfalsate"). Il prompt resta in inglese, i
generatori rendono meglio.

```text
App icon for a desktop app called "NOMEAPP": DESCRIZIONE IN UNA RIGA.

Concept: CONCETTO. The front shape is a muted terracotta (#B9694E); the shapes behind are
quieter warm tones (dusty sand #C49A4A at low saturation and warm grey-brown #857A6C).

Style: warm, calm, editorial and slightly hand-made. Flat shapes with a subtle organic
quality — edges not perfectly geometric, as if cut from paper or drawn with a confident brush.
No gradients or only an extremely subtle one, no glossy highlights, no 3D, no drop shadows
except a barely visible soft one. Generous negative space, low visual density.

Background: rounded-square app tile (squircle) in very light warm cream (#FAF9F5) with a
hair-thin low-contrast border (#E5E2D9). Palette strictly warm and desaturated; no blue-grey,
no pure black, no neon.

Constraints: no text, no letters, no logos or symbols of existing products, no starburst or
asterisk shapes. Centered composition with about 15% padding. Must stay readable at 16×16 and
32×32 px: bold, simple silhouette, max 3 shapes. Square 1024×1024, PNG.
```

Varianti utili: tema scuro (`Background tile in warm dark grey #262624, shapes slightly
lighter, terracotta #CC7D61`), più astratta (`as simple as a pictogram`), più materica
(`visible gouache/paper-cut texture`).

Se Danilo dice "in stile Claude": riprendi questo linguaggio (crema, terracotta, forme morbide)
ma niente simbolo a raggiera/asterisco né altri elementi del marchio, e diglielo in una riga.

## Conversione

Quando arriva l'immagine (di solito un `.webp` incollato in chat, il percorso è nel messaggio):

```bash
python "C:/Users/Danil/.claude/skills/app-desktop-stile/scripts/make_icon.py" "<immagine>" "<progetto>/build"
```

Aggiungi `--trim` se l'immagine ha uno sfondo bianco attorno al riquadro arrotondato (gli
angoli devono diventare trasparenti). Lo script scrive `build/icon.png` (1024), `build/icon.ico`
(16-256) e `build/icon-preview.png`: aprila con Read e controlla che a 16/32px si legga ancora.
electron-builder prende `build/icon.ico` / `build/icon.png` da solo.
