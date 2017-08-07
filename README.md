# bustracker
TFL Bus Tracker for Raspberry PI using AdaFruit Dot Matrix Display


Enable SSH and I2C in Raspberry PI preferences

Installs https://learn.adafruit.com/matrix-7-segment-led-backpack-with-the-raspberry-pi/using-the-adafruit-library
    sudo apt-get update
    sudo apt-get install -y git build-essential python-dev python-smbus python-imaging

    git clone https://github.com/adafruit/Adafruit_Python_LED_Backpack.git
    cd Adafruit_Python_LED_Backpack
    sudo python setup.py install


At this point you should be able to run bustracker.py from the command line.

To run it as a service copy app to /usr/local/bin/bustracker and daemon to /etc/init.d

Make daemon startable:
systemctl enable bustracker.sh

Then:
/etc/init.d/bustracker.sh start

It should restart on reboot
