1..300 | ForEach-Object { curl.exe -s --max-time 10 -o NUL -w "%{http_code} %{time_total}s\n" http://localhost:9899/; Start-Sleep -Milliseconds 200 }
