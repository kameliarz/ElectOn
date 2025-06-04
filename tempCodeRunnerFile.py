import pandas as pd
import os
from tabulate import tabulate


def bounded_knapsack(capacity, items):
    n = len(items)
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
def optimalkan(username):
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
        print(data)
        kapasitasmax = int(df_kpst.loc[df_kpst['pemilik'] == username, 'kapasitasdayamax'].values[0])
        print(f"Kapasitas daya max Anda :\t{kapasitasmax} watt")
        
        while(True):
            konfirmasi = input(f"Lakukan optimasi? (y/n): ").lower()
            if konfirmasi == 'y':
                items = []
                asli_data = []  # menyimpan asal usul index ke data asli
                for idx, row in pemilikbrg.iterrows():
                    for _ in range(int(row['jumlah'])):
                        items.append((row['namabarang'], row['kapasitasdaya'], row['prioritas']))
                        asli_data.append(row)

                # Jalankan knapsack
                total_value, selected_indices = bounded_knapsack(kapasitasmax, items)

                # Rekap hasil
                from collections import defaultdict

                hasil = defaultdict(int)
                total_kapasitas = 0

                for idx in selected_indices:
                    barang = items[idx]
                    hasil[barang[0]] += 1
                    total_kapasitas += barang[1]

                # Siapkan tabel
                tabel = []
                no = 1
                for nama, jumlah in hasil.items():
                    satuan_daya = df_brg[df_brg['namabarang'] == nama]['kapasitasdaya'].values[0]
                    satuan_nilai = df_brg[df_brg['namabarang'] == nama]['prioritas'].values[0]
                    tabel.append([
                        no,
                        nama,
                        jumlah,
                        satuan_daya,
                        jumlah * satuan_daya,
                        satuan_nilai,
                        jumlah * satuan_nilai
                    ])
                    no += 1

                # Tambahkan baris total
                tabel.append([
                    '--------', '----------------', '-----------------', '-----------------', '--------------------','---------------------', '--------------'
                ])
                tabel.append([
                    '', 'Total', '', '', total_kapasitas, '', total_value
                ])

                print("\nRincian Barang Terpilih:")
                print(tabulate(tabel, headers=["No.", "Nama Barang", "Jumlah Diambil", "Daya per Item (Watt)", "Total Daya (Watt)", "Prioritas per Item", "Total Nilai"], tablefmt="github"))

                break
            elif konfirmasi == 'n':
                print("|   Optimalisasi dibatalkan.")
                print("\n|   Anda akan diarahkan ke menu utama\n(Enter untuk melanjutkan.)")
                input()
                break
            else :
                print("\n|   Maaf inputan tidak sesuai, silahkan masukkan inputan yang sesuai. \n(Enter untuk melanjutkan.)")
                input()

optimalkan('lia')