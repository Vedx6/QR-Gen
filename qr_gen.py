import os
import sys
import time
import shutil
import qrcode
import requests
from PIL import Image
from datetime import datetime

# Colors
R = '\033[1;31m'
G = '\033[1;32m'
C = '\033[1;36m'
Y = '\033[1;33m'
B = '\033[1;34m'
W = '\033[0m'

# =========================
# Banner
# =========================
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{C}
  ░██████   ░█████████            ░██████                        
 ░██   ░██  ░██     ░██          ░██   ░██                       
░██     ░██ ░██     ░██         ░██         ░███████  ░████████  
░██     ░██ ░█████████  ░██████ ░██  █████ ░██    ░██ ░██    ░██ 
░██     ░██ ░██   ░██           ░██     ██ ░█████████ ░██    ░██ 
 ░██   ░██  ░██    ░██           ░██  ░███ ░██        ░██    ░██ 
  ░██████   ░██     ░██           ░█████░█  ░███████  ░██    ░██ 
       ░██                                                       
        ░██ 
{B}     ╔════════════════════════════════════════════════════╗
     ║     {Y}QR-Code Tool by Vedx{B} - {R}Black Hat{B}               ║
     ╠════════════════════════════════════════════════════╣
     ║  {C} [1] {G}Generate QR from Text                        {B}║
     ║  {C} [2] {G}Generate QR from Text File                   {B}║
     ║  {C} [3] {G}Decode QR from Image (Online)                {B}║
     ║  {C} [4] {G}Save Results to Storage                      {B}║
     ║  {Y} [0] {R}Exit                                         {B}║
     ╚════════════════════════════════════════════════════╝{W}
""")

# Generate QR from Text
def generate_qr_text():
    try:
        data = input(f"{Y}[>] Enter text (leave empty to cancel): {W}\n")
        if data.strip() == "":
            print(f"{R}[!] Cancelled by user.{W}")
            return
        
        save_confirmation = input(f"\n{Y}[>] Do you want to save the QR image? (y/n): {W}")
        if save_confirmation.lower() != 'y':
            print(f"{R}[!] Image not saved.{W}")
            return
        
        folder = "results"
        os.makedirs(folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{folder}/qrcode_{timestamp}.png"
        
        img = qrcode.make(data)
        img.save(filename)
        print(f"{G}[✓] QR-Code successfully created and saved: {filename}{W}")
    
    except KeyboardInterrupt:
        print(f"\n{R}[!] Cancelled.{W}")

# Generate QR from Text File
def generate_qr_file():
    try:
        path = input(f"{Y}[>] Enter path to text file: {W}\n")
        if not os.path.exists(path):
            print(f"{R}[!] File not found.{W}")
            return
        
        with open(path, 'r') as f:
            data = f.read().strip()
        
        if data == "":
            print(f"{R}[!] File is empty, cannot generate QR-Code.{W}")
            return

        confirm = input(f"{Y}[>] Do you want to save the QR from this file? (y/n): {W}")
        if confirm.lower() != 'y':
            print(f"{R}[!] Cancelled. Image not saved.{W}")
            return

        folder = "results"
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{folder}/qrcode_file_{timestamp}.png"

        img = qrcode.make(data)
        img.save(filename)
        print(f"{G}[✓] QR-Code successfully created and saved: {filename}{W}")

    except KeyboardInterrupt:
        print(f"\n{R}[!] Cancelled.{W}")

# Decode QR using Online API
def decode_qr_online():
    try:
        folder_qr = "results"

        file_list = [f for f in os.listdir(folder_qr) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not file_list:
            print(f"{R}[!] No QR images found in {folder_qr}.{W}")
            return

        print(f"{Y}Available QR images in {folder_qr}:{W}")
        for i, file in enumerate(file_list):
            print(f"{G}[{i+1}] {file}{W}")

        pilih = input(f"\n{Y}[>] Enter the number of the QR file to decode: {W}")
        if not pilih.isdigit() or int(pilih) < 1 or int(pilih) > len(file_list):
            print(f"{R}[!] Invalid choice.{W}")
            return
        
        filename = file_list[int(pilih)-1]
        path = os.path.join(folder_qr, filename)

        with open(path, 'rb') as img_file:
            files = {'file': img_file}
            print(f"{B}[•] Sending image to decode API...{W}\n")
            response = requests.post('https://api.qrserver.com/v1/read-qr-code/', files=files)

            if response.status_code == 200:
                result = response.json()[0]['symbol'][0]['data']
                if result:
                    print(f"{G}[✓] Decoded Result: {W}{result}")
                    
                    os.makedirs("results2", exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    result_file = f"results2/decode_result_{timestamp}.txt"
                    with open(result_file, 'w') as f:
                        f.write(result)
                    
                    print(f"{G}[✓] Decoded result saved to: {result_file}{W}")
                else:
                    print(f"{R}[!] Failed to decode QR from image.{W}")
            else:
                print(f"{R}[!] Failed to connect to API (status: {response.status_code}){W}")

    except KeyboardInterrupt:
        print(f"\n{R}[!] Cancelled by user.{W}")

# Save results to storage (copy from results/ to results2/)
def save_to_storage():
    try:
        source_folder = "results"
        target_folder = "results2"

        os.makedirs(target_folder, exist_ok=True)

        for file_name in os.listdir(source_folder):
            source_path = os.path.join(source_folder, file_name)
            target_path = os.path.join(target_folder, file_name)
            shutil.copy2(source_path, target_path)

        print(f"\n{G}[✓] All QR results copied to: {target_folder}\n")
    except Exception as e:
        print(f"{Y}[!] Failed to copy results: {str(e)}")

# Main Program
def main():
    try:
        while True:
            banner()
            choice = input(f"{G}[?] Select menu option: {W}")
            if choice == "1":
                generate_qr_text()
            elif choice == "2":
                generate_qr_file()
            elif choice == "3":
                decode_qr_online()
            elif choice == "4":
                save_to_storage()
            elif choice == "0":
                print(f"{Y}[✓] Thank you for using QR Generator!{W}")
                sys.exit()
            else:
                print(f"{R}[!] Invalid option!{W}")
            input(f"{B}Press Enter to return to menu...{W}")
    except KeyboardInterrupt:
        print(f"\n{R}[!] Exiting program...{W}")
        sys.exit()

if __name__ == "__main__":
    main()
