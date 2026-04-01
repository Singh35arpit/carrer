# Quick Installation Script for Resume Analyzer
Write-Host "Installing Resume Analyzer Dependencies..." -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Installing spaCy..." -ForegroundColor Yellow
pip install spacy

Write-Host ""
Write-Host "2. Installing PyPDF2..." -ForegroundColor Yellow
pip install PyPDF2

Write-Host ""
Write-Host "3. Installing python-docx..." -ForegroundColor Yellow
pip install python-docx

Write-Host ""
Write-Host "4. Downloading spaCy English model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run the web app:" -ForegroundColor Cyan
Write-Host "python web_app.py" -ForegroundColor White
Write-Host ""
Write-Host "Then go to: http://localhost:5000/dashboard" -ForegroundColor Cyan
Write-Host ""
