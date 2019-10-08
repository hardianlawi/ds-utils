# Install Redis
sudo apt install make gcc tcl
curl -s -o redis-stable.tar.gz http://download.redis.io/redis-stable.tar.gz
tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd /usr/local/lib/redis-stable/
make && make install
cd
