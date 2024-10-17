from pymavlink import mavutil
import sys, math, time
from Komutlar import *
import HavaSartlari

if HavaSartlari.UcusaUygunMu(50):
    # Bağlantı yapma
    try:
        drone = mavutil.mavlink_connection('127.0.0.1:14550') #Local IP + MavlinkPort
        drone.wait_heartbeat() #Sinyal Dönmesini Bekle
        print("Baglandi")
    except Exception as e:
        print(f"Baglanti hatasi: {e}")
        sys.exit(1)

    # Arm ve kalkış
    ArmVeTakeoff(drone, 20)

    #Baslangıç konumunu al
    baslangicLat, baslangicLon, baslangicAlt = KonumAl(drone)

    # 20 metre kuzeye, 30 metre batıya, 5 metre yukarı git
    Git(drone, 20, -30, 5)

    #Eve dönme gonksiyonu
    EveDon(drone, baslangicLat, baslangicLon, baslangicAlt)

    # İniş ve disarm
    KonVeDisarm(drone)