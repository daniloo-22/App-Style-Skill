# Installs a new build over the running app without losing anything.
#   powershell -ExecutionPolicy Bypass -File install-update.ps1 -AppName NomeApp -Installer "C:\...\dist\NomeApp Setup 1.0.0.exe"
# 1. closes the app like the X button (it saves its state), never a forced kill
# 2. backs up the state JSON files from %APPDATA%\<AppName>
# 3. runs the one-click installer and waits for it
# 4. reopens the app from its desktop shortcut
param(
  [Parameter(Mandatory = $true)][string]$AppName,
  [Parameter(Mandatory = $true)][string]$Installer
)

if (-not (Test-Path $Installer)) { throw "Installer non trovato: $Installer" }

$running = Get-Process -Name $AppName -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
foreach ($p in $running) {
  $p.CloseMainWindow() | Out-Null
  if ($p.WaitForExit(15000)) { "chiuso $($p.Id)" } else { throw "L'app non si e' chiusa entro 15 s (PID $($p.Id)): chiudila a mano e riprova" }
}

$data = Join-Path $env:APPDATA $AppName
if (Test-Path $data) {
  $backup = Join-Path $data ("backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
  New-Item -ItemType Directory -Force $backup | Out-Null
  Copy-Item (Join-Path $data '*.json') $backup -ErrorAction SilentlyContinue
  "backup: $backup"
}

$setup = Start-Process -FilePath $Installer -PassThru
if (-not $setup.WaitForExit(300000)) { throw "Installer ancora in corso dopo 5 minuti" }
"installer exit $($setup.ExitCode)"

$shortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) "$AppName.lnk"
if (Test-Path $shortcut) { Start-Process $shortcut; "riaperta" } else { "collegamento non trovato: $shortcut" }
