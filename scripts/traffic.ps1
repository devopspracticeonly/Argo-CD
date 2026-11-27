1..120 | ForEach-Object {
    curl.exe -s --max-time 8 -o NUL -w "%{http_code}\n" http://localhost:9696/
    Start-Sleep -Seconds 1
}
