import pandas as pd
from datetime import datetime
import os
from tabulate import tabulate
from collections import defaultdict

#==================================================================
# ALGORITMA
#==================================================================
def bounded_knapsack(capacity, items):
    dp = [0] * (capacity + 1)
    track = [[] for _ in range(capacity + 1)]

    for idx, (name, weight, value) in enumerate(items):
        for c in range(capacity, weight - 1, -1):
            if dp[c - weight] + value > dp[c]:
                dp[c] = dp[c - weight] + value
                track[c] = track[c - weight] + [idx]

    best_capacity = max(range(capacity + 1), key=lambda x: dp[x])
    best_value = dp[best_capacity]
    selected_indices = track[best_capacity]

    return best_value, selected_indices


#==================================================================
# USER
#==================================================================
def simulasi_biaya(username):
    pass

def optimalkan(username):
    header("Optimalkan Penggunaan Peralatan Elektronik")
    df_brg = pd.read_csv("databarang.csv")
    df_kpst = pd.read_csv("kapasitasdayamax.csv")
    pemilikbrg = df_brg[df_brg["pemilik"] == username]
    pemilikkpst = df_kpst[df_kpst["pemilik"] == username]
    if pemilikbrg.empty or pemilikkpst.empty:
        if pemilikbrg.empty and pemilikkpst.empty:
            print("Anda belum menginputkan barang dan kapasitas daya max yang anda miliki.\n\nSilahkan kembali dan pilih opsi 'Atur Data Barang Elektronik' di Menu Utama untuk menginputkan data barang Anda \nDan silahkan pilih opsi 'Atur Kapasitas Daya' di Menu Utama untuk menginputkan kapasitas daya max Anda.")
        elif pemilikbrg.empty:
            print("Anda belum menginputkan barang yang anda miliki.\n\nSilahkan kembali dan pilih opsi 'Atur Data Barang Elektronik' di Menu Utama untuk menginputkan data barang Anda.")
        elif pemilikkpst.empty:
            print("Anda belum menginputkan barang yang anda miliki.\n\nSilahkan kembali dan pilih opsi 'Atur Kapasitas Daya' di Menu Utama untuk menginputkan kapasitas daya max Anda.")
        print("\n(Enter untuk melanjutkan.)")
        input()
    else :
        print("Data barang Anda yang akan dioptimalisasikan : ")
        data = pemilikbrg[['namabarang', 'kapasitasdaya', 'prioritas', 'jumlah']]
        print(tabulate(data, headers='keys', tablefmt='grid'))
        kapasitasmax = int(df_kpst.loc[df_kpst['pemilik'] == username, 'kapasitasdayamax'].values[0])
        print(f"\nKapasitas daya max Anda :\t{kapasitasmax} watt")

        while(True):
            waktu_penggunaan = {}
            print("\n\nSilakan masukkan waktu penggunaan tiap barang (jam 0–23, pisahkan dengan spasi)\nmisal :   Masukkan jam penggunaan untuk kipas angin : 9 10 11 12 13 14\n")
            for idx, row in pemilikbrg.iterrows():
                nama_barang = row['namabarang']
                waktu_barang = []

                while True:
                    jam_str = input(f"Masukkan jam penggunaan untuk '{nama_barang}': ")
                    try:
                        jam_list = [int(jam) for jam in jam_str.strip().split() if 0 <= int(jam) <= 23]
                    except ValueError:
                        print("|   Input tidak valid. Gunakan angka 0–23 dipisahkan spasi.")
                        continue

                    waktu_barang.extend(jam_list)

                    tambah = input(f"Ada jam penggunaan tambahan untuk '{nama_barang}'? (y/n): ").lower()
                    if tambah == 'y':
                        continue
                    elif tambah == 'n':
                        break
                    else:
                        print("|   Input tidak valid. Dianggap 'tidak'.")
                        break

                waktu_penggunaan[nama_barang] = waktu_barang

            print("\nData waktu penggunaan yang berhasil dicatat:")
            for barang, jam in waktu_penggunaan.items():
                print(f"- {barang}: {sorted(set(jam))} jam")

            konfirmasi = input(f"Lakukan optimasi? (y/n): ").lower()
            if konfirmasi == 'y':
                hasil_optimasi_per_jam = {}
                for jam in range(24):
                    items_jam = []
                    for idx, row in pemilikbrg.iterrows():
                        nama = row['namabarang']
                        if jam in waktu_penggunaan.get(nama, []):
                            for _ in range(int(row['jumlah'])):
                                items_jam.append((nama, row['kapasitasdaya'], row['prioritas']))

                    if items_jam:
                        total_nilai, selected_indices = bounded_knapsack(kapasitasmax, items_jam)
                        hasil = defaultdict(int)
                        total_kapasitas = 0
                        for idx in selected_indices:
                            barang = items_jam[idx]
                            hasil[barang[0]] += 1
                            total_kapasitas += barang[1]
                        hasil_optimasi_per_jam[jam] = (total_kapasitas, total_nilai, hasil)

                print("\nHasil Optimasi per Jam:")
                tabel = []
                for jam in range(24):
                    if jam in hasil_optimasi_per_jam:
                        total_daya, total_nilai, hasil = hasil_optimasi_per_jam[jam]
                        daftar_barang = ", ".join([f"{nama} ({jumlah})" for nama, jumlah in hasil.items()])
                        tabel.append([jam, total_daya, total_nilai, daftar_barang])
                print(tabulate(tabel, headers=["Jam", "Total Daya", "Total Nilai", "Barang Terpilih"], tablefmt="grid"))

                print("\n|   Anda akan diarahkan ke menu utama\n(Enter untuk melanjutkan.)")
                input()
                menu_utama(username)
                break
            elif konfirmasi == 'n':
                print("|   Optimalisasi dibatalkan.")
                print("\n|   Anda akan diarahkan ke menu utama\n(Enter untuk melanjutkan.)")
                menu_utama(username)
                input()
                break
            else :
                print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai. \n(Enter untuk melanjutkan.)")
                input()

def kapasitas_daya_max(username):
    header("Atur Kapasitas Daya")
    df = pd.read_csv("kapasitasdayamax.csv")
    try:
        pemilik = df[df["pemilik"] == username]
        if pemilik.empty:
            print("Anda belum pernah menginputkan kapasitas daya rumah Anda.")
            while(True):
                inputan1 = input("Apakah Anda mau memasukkan kapasitas daya max Anda? (y/n)").lower()
                if inputan1 == 'y':
                    print("[1] 450 VA (360 watt)\n[2] 900 VA (720 watt)\n[3] 1300 VA (1040 watt)\n[4] 2200 VA (1760 watt)")
                    kapasitas = int(input("Masukkan kapasitas daya Anda (1/2/3/4): "))
                    match kapasitas:
                        case 1:
                            kapasitaswatt = 360
                        case 2:
                            kapasitaswatt = 720
                        case 3:
                            kapasitaswatt = 1040
                        case 4:
                            kapasitaswatt = 2200
                        case _:
                            print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
                            print("(Enter untuk melanjutkan.)")
                            input()   
                    data_baru = pd.DataFrame([{
                        'pemilik' : username,
                        'kapasitasdayamax' : kapasitaswatt
                    }])
                    data_baru.to_csv('kapasitasdayamax.csv', mode='a', index=False, header=False)
                    kapasitas_daya_max()
                    break
                else :
                    print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
                    print("(Enter untuk melanjutkan.)")
                    input()
        else :
            data = int(df.loc[df['pemilik'] == username, 'kapasitasdayamax'].values[0])
            print(f"Kapasitas daya max Anda :\t{data} watt")
            while(True):
                inputan2 = input("\nApakah Anda ingin mengubah kapasitas daya max Anda? (y/n)").lower()
                if inputan2 == 'y':
                    while(True):
                        print("Untuk mengganti kapasitas daya, Anda hanya diperbolehkan untuk mengganti pada kapasitas yang lebih tinggi.")
                        print("[1] 450 VA (360 watt)\n[2] 900 VA (720 watt)\n[3] 1300 VA (1040 watt)\n[4] 2200 VA (1760 watt)")
                        pilihan = int(input())
                        match pilihan:
                            case 1:
                                kapasitaswatt = 360
                            case 2:
                                kapasitaswatt = 720
                            case 3:
                                kapasitaswatt = 1040
                            case 4:
                                kapasitaswatt = 2200
                            case _:
                                print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
                                print("(Enter untuk melanjutkan.)")
                                input()  
                        if kapasitaswatt <= data :
                            print("Maaf, Anda tidak bisa mengubah kapasitas. Silahkan pilih kapasitas yang lebih tinggi dari kapasitas Anda sebelumnya.")
                        else : break   

                    df.loc[df['pemilik'] == username, 'kapasitasdayamax'] = kapasitaswatt
                    df.to_csv("kapasitasdayamax.csv", index=False)
                    print("\n|   Kapasitas daya Anda berhasil diubah.")
                    print("(Enter untuk melanjutkan.)")
                    input()
                    menu_utama(username)
                    break
                elif inputan2 == 'n':
                    print("\n|   Anda akan diarahkan ke menu utama\n(Enter untuk melanjutkan.)")
                    input()
                    menu_utama(username)
                    break
                else :
                    print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
                    print("(Enter untuk melanjutkan.)")
                    input()
    except FileNotFoundError:
        return None
    
def atur_data_barang(username):
    while(True):
        header("Atur Data Barang Elektronik")
        df = pd.read_csv("databarang.csv")
        try:
            pemilik = df[df["pemilik"] == username]
            print("[1] Lihat Data Barang \n[2] Tambahkan Data Barang \n[3] Ubah Data Barang \n[4] Hapus Data Barang \n[0] Kembali")
            inputan1 = int(input("Silahkan pilih menu di atas (1/2/3/4/0) :"))
            match inputan1:
                case 1:
                    header("Atur Data Barang Elektronik > Lihat")
                    if pemilik.empty:
                        print("Anda belum menginputkan barang yang anda miliki.\n\nSilahkan kembali dan pilih opsi 2.")
                        print("\n(Enter untuk melanjutkan.)")
                        input()
                    else :
                        data = pemilik[['namabarang', 'kapasitasdaya', 'prioritas', 'jumlah']]
                        print(data)
                        print("\n(Enter untuk melanjutkan.)")
                        input()
                case 2:
                    header("Atur Data Barang Elektronik > Tambah")
                    while(True):
                        namabrg = input("Masukkan nama barang \t: ")
                        data_brg = df[df['pemilik'] == username]['namabarang']
                        if namabrg in data_brg:
                            print(f"|   Maaf, barang {namabrg} sudah tercatat. \nJika Anda ingin mengubah data, silahkan kembali dan pilih opsi 3")
                            print("(Enter untuk melanjutkan.)")
                            input()
                            break
                        else :
                            kapasitasbrg = int(input("Masukkan kapasitas daya barang \t: "))
                            prioritasbrg = int(input("Masukkan skala prioritas barang (1-10)\t: "))
                            jumlahbrg = int(input("Masukkan jumlah barang \t: "))

                            data_baru = pd.DataFrame([{
                                'pemilik' : username,
                                'namabarang' : namabrg,
                                'kapasitasdaya' : kapasitasbrg,
                                'prioritas' : prioritasbrg,
                                'jumlah' : jumlahbrg
                            }])

                            data_baru.to_csv('databarang.csv', mode='a', index=False, header=False)
                            while(True):
                                inputan2 = input("\nApakah ada barang yang ingin ditambahkan lagi? (y/n) : ").lower()
                                if inputan2 == 'y' or 'n':
                                    break
                                else :
                                    print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
                                    print("(Enter untuk melanjutkan.)")
                                    input()
                            if inputan2 == 'n':
                                print("\n|   Anda akan diarahkan kembali ke menu atur data. \n(Enter untuk melanjutkan.)")
                                input()
                                break   
                case 3:
                    header("Atur Data Barang Elektronik > Ubah")
                    if pemilik.empty:
                        print("Anda belum menginputkan barang yang anda miliki.\n\nSilahkan kembali dan pilih opsi 2.")
                        print("\n(Enter untuk melanjutkan.)")
                        input()
                    else :
                        data = pemilik[['namabarang', 'kapasitasdaya', 'prioritas', 'jumlah']]
                        print(data)
                        print("\nAnda bisa mengubah kapasitas daya, skala priotitas, dan jumlah dari suatu barang yang dipilih.")
                        target = input("\nMasukkan nama barang yang datanya igin Anda ubah : ").lower()

                        match = df[
                        (df['pemilik'] == username.lower()) &
                        (df['namabarang'].str.lower() == target)
                        ]

                        if match.empty:
                            print("\n|   Barang tidak ditemukan.")
                        else:
                            idx = match.index[0] 
                            new_kapasitas = int(input("Masukkan kapasitas daya baru: "))
                            new_prioritas = int(input("Masukkan prioritas baru: "))
                            new_jumlah = int(input("Masukkan jumlah baru: "))

                            df.at[idx, 'kapasitasdaya'] = new_kapasitas
                            df.at[idx, 'prioritas'] = new_prioritas
                            df.at[idx, 'jumlah'] = new_jumlah

                            df.to_csv("databarang.csv", index=False)
                            print("\n|   Data berhasil diupdate.")

                        print("\n(Enter untuk melanjutkan.)")
                        input()
                case 4:
                    header("Atur Data Barang Elektronik > Hapus")
                    if pemilik.empty:
                        print("Anda belum menginputkan barang yang anda miliki.\n\nSilahkan kembali dan pilih opsi 2.")
                        print("\n(Enter untuk melanjutkan.)")
                        input()
                    else :
                        data = pemilik[['namabarang', 'kapasitasdaya', 'prioritas', 'jumlah']]
                        print(data)

                        target = input("\nMasukkan nama barang yang datanya igin Anda hapus : ").lower()

                        match = df[
                        (df['pemilik'] == username.lower()) &
                        (df['namabarang'].str.lower() == target)
                        ]

                        if match.empty:
                            print("Data tidak ditemukan.")
                        else :
                            while(True):
                                konfirmasi = input(f"Apakah Anda yakin ingin menghapus data {target}? (y/n): ").lower()
                                if konfirmasi == 'y':
                                    df = df.drop(match.index)
                                    df.to_csv("databarang.csv", index=False)
                                    print("|   Data berhasil dihapus.")
                                    break
                                elif konfirmasi == 'n':
                                    print("|   Penghapusan dibatalkan.")
                                    break
                                else :
                                    print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai. \n(Enter untuk melanjutkan.)")
                                    input()
                        print("\n|   Anda akan diarahkan kembali ke menu atur data. \n(Enter untuk melanjutkan.)")
                        input()
                case 0:
                    menu_utama(username)
                    break
                case _:
                    print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
                    print("(Enter untuk melanjutkan.)")
                    input()
        except FileNotFoundError:
            return None

def menu_utama(namapengguna, baru=False):
    header("Menu Utama")
    if baru == False:
        print(f"Selamat datang kembali, {namapengguna}!")
    else :
        print(f"Selamat datang, {namapengguna}!")
    
    print("\n[1] Atur Data Barang Elektronik \n[2] Atur Kapasitas Daya \n[3] Optimalkan Penggunaan Peralatan Elektronik")
    print("[4] Simulasikan Biaya Listrik \n[5] Lihat Laporan \n[0] Keluar")
    inputan3 = int(input("\nSilahkan pilih menu diatas (1/2/3/4/5/0) :"))
    match inputan3:
        case 1 :
            atur_data_barang(namapengguna)
        case 2 :
            kapasitas_daya_max(namapengguna)
        case 3 :
            optimalkan(namapengguna)
        case 4 | 5:
            print("Fitur belum tersedia, anda akan diarahkan ke menu. \n(Enter untuk melanjutkan.)")
            input()
            menu_utama(namapengguna)
        case 0 :
            logout()
        case _ :
            print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
            print("(Enter untuk melanjutkan.)")
            input()


#==================================================================
# ADMIN
#==================================================================
def menu_admin(namapengguna):
    header("Menu Admin")
    print(f"Selamat datang kembali, {namapengguna}!")
    
    print("\n[1] Lihat Daftar Pengguna \n[2] Atur Biaya \n[3] Lihat Laporan \n[0] Keluar")
    inputan = int(input("\nSilahkan pilih menu diatas (1/2/3/0) :"))
    match inputan:
        case 1 | 2 | 3:
            print("Fitur belum tersedia, Anda akan diarahkan ke menu. \n(Enter untuk melanjutkan.)")
            input()
            menu_admin(namapengguna)
        case 0 :
            logout()


#==================================================================
# UMUM
#==================================================================
def homepage():
    header("Homepage")
    print("\nSelamat datang di aplikasi optimasi peralatan elektronik rumah tangga! ^-^")
    print("\n[1] Login \n[2] Sign Up \n[0] Keluar")
    pilihan = int(input("Silahkan pilih menu di atas (1/2/0) :"))

    if pilihan == 1:
        login()
    elif pilihan == 2:
        signup()
    elif pilihan == 0:
        logout()
    else :
        print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
        print("(Enter untuk melanjutkan.)")
        input()
        homepage()

def header(isi=''):
    os.system('cls')
    with open('header-electon.txt', 'r', encoding='utf-8') as file:
        filetxt = file.read()
    print(filetxt)
    width = (75-len(isi))//2
    print(" "*width+isi+" "*width)
    print('─'*75)      

def signup():
    header("Sign Up")
    print("Daftarkan akun baru Anda")
    usrnm = input("\nMasukkan username  :")
    passww = input("Masukkan password   :")

    data_baru = pd.DataFrame([{
        'username' : usrnm,
        'password' : passww,
        'role' : 'user'
    }])

    data_baru.to_csv('datapengguna.csv', mode='a', index=False, header=False)
    menu_utama(usrnm, True)

def logout():
    header('LOG OUT')
    kalimat = "Terimakasih sudah menggunakan layanan kami!"
    width = (75-len(kalimat))//2
    print('\n'+" "*width+kalimat+'\n\n'+'─'*75)

def login():
    header("Log In")
    data_pengguna = pd.read_csv('datapengguna.csv')
    username = input("Masukkan username : ")
    password = input("Masukkan password : ")
    user_data = data_pengguna[data_pengguna["username"] == username]
    if username in data_pengguna["username"].values:
        if password == user_data.iloc[0]["password"] :
            peran = user_data.iloc[0]["role"]
            if peran == 'user':
                menu_utama(username)
            else :
                menu_admin(username)
        else :
            print("Maaf, password salah")
    else :
        print("\n|   Username tidak ditemukan!")
        print("\nApakah anda ingin coba lagi?")
        while(True):
            inputan1 = input("Silahkan masukkan (y/n) :").lower()
            if inputan1 == 'y':
                login()
                break
            elif inputan1 =='n':
                print("\nApakah anda ingin registrasi?")
                while(True):
                    inputan2 = input("Silahkan masukkan (y/n) :").lower()
                    if inputan2 == 'y':
                        signup()
                        break
                    elif inputan2 =='n':
                        homepage()
                        break
                    else :
                        print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
                        print("(Enter untuk melanjutkan.)")
                        input()
                break
            else :
                print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai.")
                print("(Enter untuk melanjutkan.)")
                input()

homepage()