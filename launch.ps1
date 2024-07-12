$scripts_path='.\.venv\Scripts'
$activate_path = Join-Path $scripts_path 'Activate.ps1'
$pip_path = Join-Path $scripts_path 'pip.exe'
$pythonw_path = Join-Path $scripts_path 'pythonw.exe'

if (-Not (Test-Path $activate_path -PathType Leaf)) {
    python -m venv .\.venv
}
& $pip_path install -r .\requirements.txt
& $pythonw_path .\share_session_status.pyw