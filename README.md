--Türkçe
# Drone Simülasyonu Projesi

Bu proje, Ubuntu üzerinde ArduPilot ve Gazebo kullanarak otomatik bir drone(copter) simülasyonu gerçekleştirmektedir. Proje, Python ile yazılmış kodlar kullanarak simülasyonu otomatik hale getirir.

## Özellikler

- **Otomatik Simülasyon:** Python ile yazılmış kodlar sayesinde drone simülasyonu otomatik olarak gerçekleştirilir.
- **Hava Kontrolü:** OpenWeatherMap API kullanılarak hava durumu kontrol edilir ve uçuş esnasında bu verilere göre ayarlamalar yapılır.

## Gereksinimler

- Ubuntu işletim sistemi
- ArduPilot
- Gazebo
- Python 3.x

## Kurulum
1. **Ardupilot ve gazebo kurulumu**

  Ubuntu kurulumu sonrası yüklemeler "kurulum.txt" dosyasında paylaşılmıştır.

2. **Proje Klasörünü Klonlayın:**
   ```bash
   git clone https://github.com/metinncetinn/MavlinkCopter.git
   cd MavlinkCopter
   ```

3. **API Anahtarını Ayarlayın:**
   OpenWeatherMap API anahtarınızı `key.py` dosyasına ekleyin.

## Kullanım

Simülasyonu başlatmak için aşağıdaki komutu kullanın:
  ```bash
  python Gorevler.py
  ```

## Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen pull request gönderin veya sorunlarınızı bildirin.

--English

# Drone Simulation Project

  This project implements an automatic drone (copter) simulation using ArduPilot and Gazebo on Ubuntu. The simulation is automated through Python code, which also manages wind conditions during flight.

## Features

- **Automatic Simulation:** The drone simulation is carried out automatically through Python scripts.
- **Weather Control:** Weather conditions are monitored using the OpenWeatherMap API, and adjustments are made during flight based on this data.

## Requirements

- Ubuntu operating system
- ArduPilot
- Gazebo
- Python 3.x

## Installation
1. **Install ArduPilot and Gazebo**

  Installation instructions are provided in a "kurulum.txt" file after Ubuntu installation.

2. **Clone the Project Folder:**
   ```bash
   git clone https://github.com/metinncetinn/MavlinkCopter.git
   cd MavlinkCopter
   ```

3. **Set Up Your API Key:**
   Add your OpenWeatherMap API key to the `key.py` file.

## Usage

To start the simulation, use the following command:
  ```bash
  python Gorevler.py
  ```

## Contributing

We welcome your contributions! Please submit pull requests or report any issues.
