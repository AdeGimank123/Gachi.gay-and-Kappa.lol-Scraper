import requests
import random
import string
from colorama import Fore, Style, init

init(autoreset=True)

def generate_random_id(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def check_page_exists(url):
    try:
        response = requests.get(url, timeout=5)
        if "Object Not Found" in response.text or response.status_code == 404:
            return False
        return True
    except requests.RequestException:
        return False

def baca_id_yg_kesimpen():
    try:
        with open("valid.txt", "r") as f:
            valid = {line.strip().split('/')[-1] for line in f}
    except FileNotFoundError:
        valid = set()

    try:
        with open("tdk_valid.txt", "r") as f:
            tdk_valid = {line.strip().split('/')[-1] for line in f}
    except FileNotFoundError:
        tdk_valid = set()

    return valid.union(tdk_valid)

def simpen_file(file, url):
    with open(file, "a") as f:
        f.write(url + "\n")

def scan_ids(base_url, quantity):
    found_ids = []
    udah_scan = baca_id_yg_kesimpen()

    for i in range(quantity):
        for length in [5, 6]:  # 5 dan 6 digit
            random_id = generate_random_id(length)
            if random_id in udah_scan:
                continue  # skip jika sudah dicek
            full_url = base_url + random_id
            print(f"[{i+1}/{quantity}] Memeriksa ({length} digit): {full_url}")

            if check_page_exists(full_url):
                print(Fore.GREEN + "  >> FILE DITEMUKAN!")
                found_ids.append(full_url)
                simpen_file("valid.txt", full_url)
            else:
                print(Fore.RED + "  >> 404 / Tidak ditemukan")
                simpen_file("tdk_valid.txt", full_url)

    print("\n=== PENCARIAN SELESAI ===")
    if found_ids:
        print(Fore.GREEN + "ID yang ditemukan:")
        for url in found_ids:
            print(Fore.GREEN + " - " + url)
    else:
        print(Fore.RED + "Tidak ada ID yang valid ditemukan.")

def test_manual_link():
    url = input("Masukkan URL (contoh: https://gachi.gay/SsilMK ): ").strip()

    if check_page_exists(url):
        print(Fore.GREEN + ">> File ditemukan!")
        simpen_file("valid.txt", url)
    else:
        print(Fore.RED + ">> 404 / Tidak ditemukan")
        simpen_file("tdk_valid.txt", url)

def main_menu():
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Scan dari gachi.gay")
        print("2. Scan dari kappa.lol")
        print("3. Tes Link manual")
        print("4. Keluar")

        choice = input("Pilih opsi (1/2/3/4): ").strip()
        if choice == "1":
            base_url = "https://gachi.gay/"
        elif choice == "2":
            base_url = "https://kappa.lol/"
        elif choice == "3":
            test_manual_link()
            continue
        elif choice == "4":
            print("Keluar.")
            break
        else:
            print("Pilihan tidak valid.")
            continue

        try:
            jumlah = int(input("Masukkan jumlah ID yang ingin discan: "))
            scan_ids(base_url, jumlah)
        except ValueError:
            print("Input harus berupa angka woi!")

        ulang = input("\nIngin mengulang pencarian? (y/n): ").lower()
        if ulang != 'y':
            print("Done!")
            break

if __name__ == "__main__":
    main_menu()
