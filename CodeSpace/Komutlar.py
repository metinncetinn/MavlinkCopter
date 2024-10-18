"""
Komutlarin linki
https://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html#set-position-target-global-int
"""

from pymavlink import mavutil
import sys, math, time

#Drondan konum bilgilerini alma
def KonumAl(drone):
    msg = drone.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    if msg:
        return msg.lat / 1e7, msg.lon / 1e7, msg.relative_alt / 1000.0
    else:
        print("Konum alinamadi")
        return None

#Dronun çalışır hale gelmesi ve yükselmesi
def ArmVeTakeoff(drone, height):
    # GUIDED MOD ALMA
    mode = 'GUIDED'
    if mode not in drone.mode_mapping():
        print('Bilinmeyen mod: {}'.format(mode))
        print('Drone modları:', list(drone.mode_mapping().keys()))
        sys.exit(1)
    mode_id = drone.mode_mapping()[mode]
    drone.mav.set_mode_send(drone.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode_id)

    # ARM ETME
    drone.mav.command_long_send(
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1,  # 1 = arm, 0 = disarm
        0, 0, 0, 0, 0, 0
    )
    
    print("Komut verildi")
    drone.motors_armed_wait() #Arm Olmayı bekle
    print("Arm gerceklesti")

    # KALKIŞIN GERÇEKLEŞMESİ
    drone.mav.command_long_send(
        drone.target_system, 
        drone.target_component, 
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 
        0, 0, 0, 0, 0, 0, 0, height
    )

    # Saniyede 1 yüksekliği al ve kalkışın tamamlandığını kontrol et
    while True:
        current_position = KonumAl(drone)
        if current_position:
            _, _, current_alt = current_position
            if current_alt >= height * 0.95:  # Yüksekliğin %95'ine ulaştıysa(hata payı/threshold)
                print("Kalkis tamamlandi.")
                break
        time.sleep(1)  # Kontrol aralığı

# Dünya yarıçapı (metre cinsinden)
#R = 6378137

#Metreyi enleme çevirme
def meters_to_lat(meters):
    return meters / 111320

#Metreyi boylama çevirme(enleme bağlı)
def meters_to_lon(meters, latitude):
    return meters / (111320 * math.cos(math.radians(latitude)))

#Dronu bulunduğu pozisyondan metre cinsinden ilerletme
def Git(drone, lat_offset, lon_offset, alt_offset):
    #Direkt kordinat verilmediği için şu anki konuma eklem yapılacak. Bu yüzden konum alınıyor.
    current_position = KonumAl(drone)
    if current_position:
        current_lat, current_lon, current_alt = current_position
        print(f"Mevcut Konum: Lat: {current_lat}, Lon: {current_lon}, Alt: {current_alt}")

        #Kordinat cinsinden metreyi hesaplama ve şu anki konuma ekleme.
        delta_lat = meters_to_lat(lat_offset)
        delta_lon = meters_to_lon(lon_offset, current_lat)

        target_lat = current_lat + delta_lat
        target_lon = current_lon + delta_lon
        target_alt = current_alt + alt_offset

        drone.mav.set_position_target_global_int_send(
            0, 
            drone.target_system, 
            drone.target_component,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            0b110111111000,  #(type_mask) Kullanılacak parametreler yukarıdaki linkte mevcut.
            int(target_lat * 1e7),
            int(target_lon * 1e7),
            target_alt,
            0, 0, 0,  # Hız (vx, vy, vz)
            0, 0,  # İvme (ax, ay)
            0, 0,  # Yaw, Yaw rate
            0  # Yaw rate
        )
        print(f"Yeni hedefe uculuyor: Lat: {target_lat}, Lon: {target_lon}, Alt: {target_alt}")

        threshold = 1.0  # 1 metre hata payı
        while True:
            cPos = KonumAl(drone)
            if cPos:
                c_lat, c_lon, c_alt = cPos
                if (abs(c_lat - target_lat) < threshold / 111320) and \
                   (abs(c_lon - target_lon) < threshold / (111320 * math.cos(math.radians(current_lat)))) and \
                   (abs(c_alt - target_alt) < threshold):
                    print("Hedefe ulasildi.")
                    break
            time.sleep(1)  # Kontrol aralığı
    else:
        print("Mevcut konum alinamadi")

#İniş ve motoru kapatma fonksiyonu
def KonVeDisarm(drone):
    mode = 'LAND'
    if mode not in drone.mode_mapping():
        print('Bilinmeyen mod: {}'.format(mode))
        print('Deneyin:', list(drone.mode_mapping().keys()))
        sys.exit(1)

    mode_id = drone.mode_mapping()[mode]
    drone.mav.set_mode_send(drone.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode_id)

    drone.mav.command_long_send(
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0,  # confirmation
        0,  # param1
        0,  # param2
        0,  # param3
        0,  # param4
        0,  # param5
        0,  # param6
        0   # param7
    )
    print("İnis komutu gonderildi.")

    while True:
        msg = drone.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg and msg.relative_alt <= 0.2:
            print("Drone inis yapti.")
            break

    drone.mav.command_long_send(
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        0,  # 0 = disarm
        0, 0, 0, 0, 0, 0
    )
    print("Disarm islemi tamamlandi.")

#İnis(kalkış pozisyonuna) ve motoru kapatma
def EveDon(drone, basLat, basLon, basAlt):
    current_position = KonumAl(drone)
    if current_position:
        current_lat, current_lon, current_alt = current_position
        print(f"Mevcut Konum: Lat: {current_lat}, Lon: {current_lon}, Alt: {current_alt}")

        drone.mav.set_position_target_global_int_send(
            0, 
            drone.target_system, 
            drone.target_component,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            0b110111111000,  # Kullanılacak parametreler
            int(basLat * 1e7),
            int(basLon * 1e7),
            basAlt,
            0, 0, 0,  # Hız (vx, vy, vz)
            0, 0,  # İvme (ax, ay)
            0, 0,  # Yaw, Yaw rate
            0  # Yaw rate
        )
        print(f"Eve uculuyor: Lat: {basLat}, Lon: {basLon}, Alt: {basAlt}")

        threshold = 1.0  # 1 metre eşiği
        while True:
            cPos = KonumAl(drone)
            if cPos:
                c_lat, c_lon, c_alt = cPos
                if (abs(c_lat - basLat) < threshold / 111320) and \
                   (abs(c_lon - basLon) < threshold / (111320 * math.cos(math.radians(current_lat)))) and \
                   (abs(c_alt - basAlt) < threshold):
                    print("Eve ulasildi.")
                    break
            time.sleep(1)  # Döngüde aşırı yüklenmeyi önlemek için bekleme
    else:
        print("Mevcut konum alinamadi")
