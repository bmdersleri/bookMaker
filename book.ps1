<#
.SYNOPSIS
    bookMaker ana komut dosyasi - kitap projesine yonlendirir.
.DESCRIPTION
    Kitap projesi book_projects/<book_name>/ altina tasinmistir.
    Bu script sizi dogru kitap projesine yonlendirir.
    
    Kullanim:
      .\book              -> kitap projesine git
      .\book status       -> kitap projesinde git status
      .\book help         -> yardim
#>

param(
    [Parameter(Position=0)]
    [string]$Command = "",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

$BOOK_PROJECT = "D:\bookMaker_Deepseek\book_projects\java-temelleri"

function Show-Help {
    Write-Host @"
bookMaker - Kitap Uretim Studyosu

KULLANIM:
  .\book                  Kitap projesine git
  .\book <komut>          Kitap projesinde komut calistir

KOMUTLAR:
  status                  Git durumu
  help                    Bu mesaj
  
ORNEKLER:
  .\book                  cd book_projects/java-temelleri
  .\book status           Git durumunu goster
  
NOT: Kitap projesi book_projects/java-temelleri/ altina tasinmistir.
Kod ve scriptler icin dogrudan proje dizinine gidin.
"@
}

if ($Command -eq "help" -or $Command -eq "--help" -or $Command -eq "-h") {
    Show-Help
    exit
}

if ($Command -eq "") {
    Write-Host "[OK] Kitap projesine yonlendiriliyor: $BOOK_PROJECT"
    Set-Location $BOOK_PROJECT
    Write-Host "[OK] Su an: $(Get-Location)"
    Write-Host "[INFO] '.\book help' ile komutlari gorun."
    exit
}

# Dogrudan kitap projesindeki book.ps1'e yonlendir
& $BOOK_PROJECT\book.ps1 @($Command) @Args
