@echo off
set /p msg="Entrer le message de commit : "
git add .
git commit -m "%msg%"
git pull
git push origin main
pause
