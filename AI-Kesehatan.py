import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Baca data dari file CSV
flpath = r"C:\Tugas Kuliah\Semester 4\Artificial Intelligent (AI)\Fuzzy\Tes 1\AI-Kesehatan.xlsx"
data = pd.read_excel(flpath)
print(data.shape)

# Definisikan variabel input
fasilitas_kesehatan = ctrl.Antecedent(np.arange(1, 6, 1), 'fasilitas_kesehatan')
tenaga_kesehatan = ctrl.Antecedent(np.arange(0, 31, 1), 'tenaga_kesehatan')
usia_penduduk = ctrl.Antecedent(np.arange(17, 91, 1), 'usia_penduduk')

# Definisikan variabel output
tingkat_pemenuhan = ctrl.Consequent(np.arange(0, 101, 1), 'tingkat_pemenuhan')

# Fungsi keanggotaan untuk variabel input dan output
fasilitas_kesehatan.automf(3)
tenaga_kesehatan.automf(3)
usia_penduduk['sehat'] = fuzz.trimf(usia_penduduk.universe, [17, 35, 50])
usia_penduduk['cenderung_sehat'] = fuzz.trimf(usia_penduduk.universe, [40, 55, 70])
usia_penduduk['rawan'] = fuzz.trimf(usia_penduduk.universe, [65, 85, 90])

tingkat_pemenuhan['memenuhi'] = fuzz.trimf(tingkat_pemenuhan.universe, [0, 33, 66])
tingkat_pemenuhan['hampir_memenuhi'] = fuzz.trimf(tingkat_pemenuhan.universe, [33, 66, 100])
tingkat_pemenuhan['kurang_memenuhi'] = fuzz.trimf(tingkat_pemenuhan.universe, [66, 100, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(fasilitas_kesehatan['poor'] | tenaga_kesehatan['poor'] | usia_penduduk['rawan'], tingkat_pemenuhan['kurang_memenuhi'])
rule2 = ctrl.Rule(fasilitas_kesehatan['average'] | tenaga_kesehatan['average'] | usia_penduduk['cenderung_sehat'], tingkat_pemenuhan['hampir_memenuhi'])
rule3 = ctrl.Rule(fasilitas_kesehatan['good'] | tenaga_kesehatan['good'] | usia_penduduk['sehat'], tingkat_pemenuhan['memenuhi'])

# Buat sistem kontrol fuzzy
tingkat_pemenuhan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tingkat_pemenuhan_sim = ctrl.ControlSystemSimulation(tingkat_pemenuhan_ctrl)

# Inisialisasi list untuk menyimpan hasil
hasil_pemenuhan = []

# Iterasi melalui setiap record dalam data
for index, row in data.iterrows():
    # Masukkan nilai variabel input dari data yang dibaca
    tingkat_pemenuhan_sim.input['fasilitas_kesehatan'] = row['fasilitas_kesehatan']
    tingkat_pemenuhan_sim.input['tenaga_kesehatan'] = row['tenaga_kesehatan']
    tingkat_pemenuhan_sim.input['usia_penduduk'] = row['usia_penduduk']

    # Hitung nilai variabel output
    tingkat_pemenuhan_sim.compute()

    # Simpan hasil
    hasil_pemenuhan.append(tingkat_pemenuhan_sim.output['tingkat_pemenuhan'])

# Tambahkan hasil ke data frame
data['tingkat_pemenuhan'] = hasil_pemenuhan

# Simpan ke file Excel
data.to_excel('hasil_AI.xlsx', index=False)
