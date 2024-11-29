akun_cashless = {}

def tambah_akun_cashless():
    print("\n" + "="*40)
    print("=== Tambah Akun Cashless ===")
    print("="*40)
    user_id = input("Masukkan ID akun baru: ")
    if user_id in akun_cashless:
        print("Akun sudah terdaftar!")
        return
    pin = input("Masukkan PIN (6 digit): ")
    saldo = input("Masukkan saldo awal: ")
    if saldo.isdigit():
        akun_cashless[user_id] = {"pin": pin, "saldo": int(saldo)}
        print("Akun berhasil ditambahkan!")
    else:
        print("Saldo harus berupa angka!")

mobil_list = {
    "Avanza": {"harga": 300000, "stok": 5},
    "Innova": {"harga": 400000, "stok": 3},
    "Fortuner": {"harga": 700000, "stok": 2},
    "Pajero": {"harga": 800000, "stok": 2},
    "Xenia": {"harga": 250000, "stok": 6}
}

biaya_supir = 150000
biaya_asuransi = 200000
denda_per_jam = 50000
mobil_dipinjam = {}

def tampilkan_daftar_mobil():
    print("\n" + "="*40)
    print("=== Daftar Mobil ===")
    print("="*40)
    print("+----+-----------+-------------------+------+")
    print("| No | Mobil     | Harga/Hari        | Stok |")
    print("+----+-----------+-------------------+------+")
    for i, (mobil, info) in enumerate(mobil_list.items(), start=1):
        print(f"| {i:<2} | {mobil:<9} | {info['harga']:<15,} IDR | {info['stok']:<4} |")
    print("+----+-----------+-------------------+------+")
    print("="*40)

def pilih_mobil():
    while True:
        pilihan = input("Pilih nomor mobil: ")
        if pilihan.isdigit():
            pilihan = int(pilihan)
            if 1 <= pilihan <= len(mobil_list):
                mobil = list(mobil_list.keys())[pilihan - 1]
                if mobil_list[mobil]["stok"] > 0:
                    return mobil
                else:
                    print("Maaf, mobil ini sedang tidak tersedia.")
            else:
                print("Pilihan tidak valid, coba lagi.")
        else:
            print("Masukkan angka yang valid.")

def input_ya_tidak(pesan):
    while True:
        pilihan = input(pesan + " (y/n): ").lower()
        if pilihan in ["y", "n"]:
            return pilihan == "y"
        print("Input tidak valid, coba lagi.")

def metode_cashless(total_bayar):
    print("\n" + "="*40)
    print("=== Pembayaran Cashless ===")
    print("="*40)
    user_id = input("Masukkan ID akun: ")
    if user_id not in akun_cashless:
        print("Akun tidak ditemukan. Tambahkan akun terlebih dahulu.")
        return False

    pin = input("Masukkan PIN (6 digit): ")
    if not (pin.isdigit() and len(pin) == 6):
        print("PIN tidak valid. PIN harus berupa angka dan terdiri dari 6 digit!")
        return False

    if akun_cashless[user_id]["pin"] != pin:
        print("PIN salah! Transaksi gagal.")
        return False

    if akun_cashless[user_id]["saldo"] < total_bayar:
        print("Saldo tidak mencukupi. Transaksi gagal.")
        return False

    akun_cashless[user_id]["saldo"] -= total_bayar
    print(f"Transaksi berhasil! Saldo tersisa: {akun_cashless[user_id]['saldo']:,} IDR")
    return True

def peminjaman():
    tampilkan_daftar_mobil()
    mobil_dipilih = pilih_mobil()
    harga_mobil = mobil_list[mobil_dipilih]["harga"]

    pakai_supir = input_ya_tidak("Apakah ingin menggunakan supir?")
    pakai_asuransi = input_ya_tidak("Apakah ingin menambahkan asuransi?")

    while True:
        hari = input(f"Berapa hari ingin menyewa {mobil_dipilih}? ")
        if hari.isdigit() and int(hari) > 0:
            hari = int(hari)
            break
        print("Masukkan jumlah hari yang valid.")

    total_sewa = harga_mobil * hari
    if pakai_supir:
        total_sewa += biaya_supir * hari
    if pakai_asuransi:
        total_sewa += biaya_asuransi

    while True:
        metode = input("Pilih metode pembayaran (cash/cashless): ").lower()
        if metode == "cash":
            print(f"Total yang harus dibayar: {total_sewa:,} IDR secara tunai.")
            if input_ya_tidak("Apakah Anda sudah membayar secara tunai?"):
                print("Pembayaran berhasil dilakukan secara tunai.")
                break
            else:
                print("Pembayaran dibatalkan.")
                return
        elif metode == "cashless":
            if metode_cashless(total_sewa):
                break
            else:
                print("Pembayaran gagal, coba metode lain.")
        else:
            print("Metode pembayaran tidak valid. Pilih 'cash' atau 'cashless'.")

    nomor_registrasi = f"{mobil_dipilih}-{len(mobil_dipinjam) + 1}"
    mobil_list[mobil_dipilih]["stok"] -= 1
    mobil_dipinjam[nomor_registrasi] = {
        "mobil": mobil_dipilih,
        "hari": hari,
        "total_bayar": total_sewa,
        "pakai_supir": pakai_supir,
        "pakai_asuransi": pakai_asuransi
    }
    print(f"\nMobil {mobil_dipilih} berhasil disewa dengan nomor registrasi {nomor_registrasi} selama {hari} hari.")
    print("="*40)

def pengembalian():
    print("\n" + "="*40)
    print("=== Pengembalian Mobil ===")
    print("="*40)
    if not mobil_dipinjam:
        print("Tidak ada mobil yang sedang dipinjam.")
        return

    print("Mobil yang sedang dipinjam:")
    for reg, data in mobil_dipinjam.items():
        print(f"- {reg} (Merk: {data['mobil']}, {data['hari']} hari, Total bayar: {data['total_bayar']:,} IDR)")

    nomor_registrasi = input("Masukkan nomor registrasi mobil yang akan dikembalikan: ")
    if nomor_registrasi not in mobil_dipinjam:
        print("Nomor registrasi tersebut tidak ditemukan dalam daftar pinjaman.")
        return

    keterlambatan = input("Berapa jam keterlambatan pengembalian? ")
    if keterlambatan.isdigit():
        keterlambatan = int(keterlambatan)
        denda = keterlambatan * denda_per_jam
    else:
        print("Input keterlambatan tidak valid.")
        return

    data_mobil = mobil_dipinjam.pop(nomor_registrasi)
    mobil_list[data_mobil["mobil"]]["stok"] += 1

    print(f"\nMobil dengan nomor registrasi {nomor_registrasi} berhasil dikembalikan.")
    print(f"Keterlambatan: {keterlambatan} jam, Denda: {denda:,} IDR")

    while True:
        metode = input("Pilih metode pembayaran untuk denda (cash/cashless): ").lower()
        if metode == "cash":
            print(f"Silakan bayar denda sebesar: {denda:,} IDR secara tunai.")
            if input_ya_tidak("Apakah Anda sudah membayar denda secara tunai?"):
                print("Pembayaran denda berhasil secara tunai.")
                break
        elif metode == "cashless":
            if metode_cashless(denda):
                break
            else:
                print("Pembayaran gagal, coba metode lain.")
        else:
            print("Metode pembayaran tidak valid. Pilih 'cash' atau 'cashless'.")

def main():
    while True:
        print("\n" + "="*40)
        print("=== Menu ===")
        print("="*40)
        print("1. Peminjaman")
        print("2. Pengembalian")
        print("3. Tambah Akun Cashless")
        print("4. Keluar")
        print("="*40)
        
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            peminjaman()
        elif pilihan == "2":
            pengembalian()
        elif pilihan == "3":
            tambah_akun_cashless()
        elif pilihan == "4":
            print("Terima kasih telah menggunakan layanan kami.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

main()