sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install libusb-dev  -y
sudo apt-get install libdbus-1-dev  -y
sudo apt-get install libglib2.0-dev --fix-missing -y
sudo apt-get install libudev-dev -y 
sudo apt-get install libical-dev -y
sudo apt-get install libreadline-dev -y
sudo apt-get install libdbus-glib-1-dev -y

mkdir bluez
cd bluez
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.30.tar.xz
gunzip bluez-5.30.tar.xz
tar xvf bluez-5.30.tar.xz
cd bluez-5.30
./configure --disable-systemd
make
sudo make install

sudo apt-get install python-bluez

cd ../../blescan/
git clone https://github.com/switchdoclabs/iBeacon-Scanner-.git
ln -s iBeacon-Scanner-/blescan.py blescan.py

echo "You must restart pi"
echo "sudo shutdown -r now"

