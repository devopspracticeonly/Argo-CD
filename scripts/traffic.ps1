1..600 | ForEach-Object { curl.exe -s --max-time 8 -o NUL -w "%{http_code} %{time_total}s\n" http://localhost:9906/; Start-Sleep -Seconds 1 }
