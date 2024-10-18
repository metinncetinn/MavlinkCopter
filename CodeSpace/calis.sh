# Gazebo terminali
gnome-terminal -- bash -c "cd && gz sim -v4 -r iris_runway.sdf; exec bash"
sleep 10  # Gazebo'yu 10 saniye bekle

# ArduPilot terminali
gnome-terminal -- bash -c "cd ~/ardupilot/Tools/autotest && python sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console; exec bash"
