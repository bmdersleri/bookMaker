# Find empty directories in bookMaker project
param([string]$Root = "D:\bookMaker_Deepseek")
$exclude = @('.git','.venv','node_modules','__pycache__','.pytest_cache','.ruff_cache')

Get-ChildItem $Root -Recurse -Directory -Exclude $exclude | Where-Object {
    (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue).Count -eq 0
} | ForEach-Object {
    Write-Host $_.FullName
}
