<#
.SYNOPSIS
    bookMaker — Tek script ile tum islemler.
.DESCRIPTION
    Kullanim:
      .\book batch 3           # Batch 3 calistir (P1-P12 combined prompt)
      .\book batch 3 --two-step # Iki asamali mod
      .\book build             # Kitap birlestir + DOCX
      .\book build --md        # Sadece Markdown
      .\book status            # Git durumu
      .\book push              # Stage + commit (interaktif) + push
      .\book test              # Testleri calistir (fast secenegi)
      .\book test --all        # Tum testler
      .\book lint              # Ruff lint
      .\book fmt               # Ruff format
      .\book check             # Kitap butunluk kontrolu
      .\book log               # Git log (son 10)
      .\book help              # Bu mesaj
.PARAMETER Command
    Yapilacak islem: batch, build, status, push, test, lint, fmt, check, log, help
.PARAMETER Args
    Komuta ozel argumanlar
.EXAMPLE
    .\book batch 3
    .\book build
    .\book push "feat: chapter 24 added"
#>

param(
    [Parameter(Position=0)]
    [string]$Command = "help",

    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

$ROOT = $PSScriptRoot
$PY = Join-Path $ROOT ".venv" "Scripts" "python.exe"

function Write-Step {
    param([string]$Msg, [string]$Color = "Green")
    Write-Host "==> $Msg" -ForegroundColor $Color
}

function Write-Error {
    param([string]$Msg)
    Write-Host "HATA: $Msg" -ForegroundColor Red
}

# ============================================================
# KOMUTLAR
# ============================================================

switch ($Command.ToLower()) {

    "batch" {
        if (-not (Test-Path $PY)) {
            Write-Error "Python venv bulunamadi: $PY"
            exit 1
        }
        $batchNum = if ($Args.Count -gt 0 -and $Args[0] -notlike "-*") { $Args[0] } else { "" }
        $extraArgs = $Args | Where-Object { $_ -ne $batchNum }
        $batchFlag = if ($batchNum) { "--batch $batchNum" } else { "" }

        Write-Step "Batch $batchNum baslatiliyor... (extra: $extraArgs)"
        $cmd = "& `"$PY`" tools/batch/batch_v2.py $batchFlag $extraArgs"
        Write-Host "  $cmd" -ForegroundColor Gray
        Invoke-Expression $cmd
    }

    "build" {
        if (-not (Test-Path $PY)) {
            Write-Error "Python venv bulunamadi: $PY"
            exit 1
        }
        $format = "both"
        if ($Args -contains "--md") { $format = "md" }
        if ($Args -contains "--docx") { $format = "docx" }

        Write-Step "Kitap birlestiriliyor... (format: $format)"
        & $PY tools/build/book_build.py --format $format
    }

    "pdf" {
        if (-not (Test-Path $PY)) {
            Write-Error "Python venv bulunamadi: $PY"
            exit 1
        }
        Write-Step "PDF uretiliyor (pandoc + xelatex)..."
        & $PY tools/build/book_pdf_v3.py
    }

    "status" {
        Write-Step "Git durumu"
        git -C $ROOT status --short
    }

    "push" {
        $msg = if ($Args.Count -gt 0) { $Args -join " " } else { $null }
        
        Write-Step "Her sey stage'leniyor..."
        git -C $ROOT add -A
        
        $status = git -C $ROOT status --short
        if (-not $status) {
            Write-Host "  Commitlecek bir sey yok." -ForegroundColor Yellow
            exit 0
        }
        
        Write-Host "  Stage'lenen dosyalar:" -ForegroundColor Gray
        Write-Host $status -ForegroundColor DarkGray
        
        if (-not $msg) {
            # Interaktif commit mesaji
            $msg = Read-Host "Commit mesaji (bos = otomatik): "
        }
        if (-not $msg) {
            $msg = "feat: auto-commit ($(Get-Date -Format 'yyyy-MM-dd HH:mm'))"
            Write-Host "  Otomatik mesaj: $msg" -ForegroundColor Yellow
        }
        
        Write-Step "Commit: $msg"
        git -C $ROOT commit -m $msg
        
        Write-Step "Push ediliyor..."
        git -C $ROOT push origin deepseek
    }

    "test" {
        if (-not (Test-Path $PY)) {
            Write-Error "Python venv bulunamadi: $PY"
            exit 1
        }
        if ($Args -contains "--all") {
            Write-Step "Tum testler calistiriliyor..."
            & $PY -m pytest tests/ -q --tb=short
        } else {
            Write-Step "Hizli testler calistiriliyor..."
            & $PY -m pytest tests/ -q --tb=short -m "not slow"
        }
    }

    "lint" {
        if (-not (Test-Path $PY)) {
            Write-Error "Python venv bulunamadi: $PY"
            exit 1
        }
        Write-Step "Ruff lint..."
        & $PY -m ruff check src/ tests/
    }

    "fmt" {
        if (-not (Test-Path $PY)) {
            Write-Error "Python venv bulunamadi: $PY"
            exit 1
        }
        Write-Step "Ruff format..."
        & $PY -m ruff format src/ tests/
    }

    "check" {
        Write-Step "Kitap kontrolu"
        $total = 0
        $order = @(
            "bolum-01","bolum-02","bolum-03","bolum-04","bolum-05","bolum-06",
            "bolum-07","bolum-08","bolum-09","bolum-10","bolum-11",
            "bolum-12","bolum-13","bolum-14","bolum-15","bolum-16",
            "bolum-17","bolum-18","bolum-19","bolum-20","bolum-21",
            "bolum-22","bolum-23",
            "ek-a","ek-b","ek-c","ek-d"
        )
        
        $ok = 0; $missing = 0; $empty = 0
        $min_target = 10000
        foreach ($ch in $order) {
            $path = Join-Path $ROOT "chapters" $ch "draft_versions" "v001.md"
            if (-not (Test-Path $path)) {
                Write-Host "  [  ] $ch — KAYIP" -ForegroundColor Red
                $missing++
                continue
            }
            $len = (Get-Item $path).Length
            $total += $len
            $ok++
            $flag = if ($len -lt $min_target) { " AZ ($len bytes < $min_target)" } else { "" }
            $color = if ($len -ge $min_target) { "Green" } else { "Yellow" }
            Write-Host "  [OK] $ch — $($len.ToString('N0')) bytes$flag" -ForegroundColor $color
        }
        
        Write-Host "`n  OZET:" -ForegroundColor Cyan
        Write-Host "    Mevcut : $ok / $($order.Count)" -ForegroundColor $(if ($ok -eq $order.Count) { "Green" } else { "Yellow" })
        Write-Host "    Kayip  : $missing" -ForegroundColor $(if ($missing -eq 0) { "Green" } else { "Red" })
        Write-Host "    Toplam : $($total.ToString('N0')) bytes"
        Write-Host "    Ortalama: $(($total / [math]::Max(1,$ok)).ToString('N0')) bytes/bolum"
    }

    "log" {
        $n = if ($Args.Count -gt 0 -and $Args[0] -match '^\d+$') { $Args[0] } else { 10 }
        Write-Step "Git log (son $n)"
        git -C $ROOT log --oneline -$n
    }

    "help" {
        Write-Host @"

╔══════════════════════════════════════════════════════════╗
║              bookMaker — Hizli Komutlar                 ║
╚══════════════════════════════════════════════════════════╝

KULLANIM:
  .\book <komut> [argumanlar]

KOMUTLAR:

  batch [N]              Batch N'i calistir (P1-P12 combined)
    --two-step           Iki asamali mod (outline+chapter ayri)
    orn: .\book batch 3
    orn: .\book batch 4 --two-step

  build [--md|--docx]    Kitap birlestir + DOCX (varsayilan: both)
    orn: .\book build
    orn: .\book build --md

  status                 Git durumu (degisen dosyalar)

  push [mesaj]           Stage + commit + push
    orn: .\book push
    orn: .\book push "feat: new chapter"

  test [--all]           Testleri calistir
    orn: .\book test           # hizli (not slow)
    orn: .\book test --all     # tumu

  lint                   Ruff lint kontrolu
  fmt                    Ruff format
  check                  Kitap butunluk kontrolu (tum bolumler)
  pdf                    PDF ciktisi (pandoc + xelatex, 54 Mermaid PNG)
  log [N]                Git log (son N commit, varsayilan: 10)

  help                   Bu mesaj

HEDEFLER:
  -. 24 bolum + 4 ek = ~552K karakter kitap
  -. GitHub: https://github.com/bmdersleri/bookMaker
  -. Branch: deepseek

"@
    }

    default {
        Write-Error "Bilinmeyen komut: $Command"
        Write-Host "Kullanilabilir: batch, build, pdf, status, push, test, lint, fmt, check, log, help"
    }
}
