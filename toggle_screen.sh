sudo bash << EOF 
echo "17" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio17/direction
echo "1" > /sys/class/gpio/gpio17/value
sleep 0.1
echo "0" > /sys/class/gpio/gpio17/value