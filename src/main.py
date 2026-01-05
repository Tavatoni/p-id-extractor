import os
import cv2
import re
import numpy as np
import pandas as pd
import glob
import gc
from pdf2image import convert_from_path
from paddleocr import PaddleOCR

# Inisialisasi OCR
ocr_engine = PaddleOCR(use_textline_orientation=True, lang='en')

def extract_page_number(filename):
    match = re.search(r'pages-(\d+)', filename)
    return int(match.group(1)) if match else 0

def get_text_from_prediction(prediction):
    texts = []
    if prediction and len(prediction) > 0:
        for res in prediction:
            if res:
                for line in res:
                    texts.append(line[1][0])
    return texts

def main():
    input_pattern = "data/input/P&ID Ammonia AFC-5-pages-*.pdf"
    output_file = "data/output/DEBUG_Daftar_Equipment.xlsx"
    # Kita tes hanya 5 halaman pertama dulu agar cepat
    pdf_files = sorted(glob.glob(input_pattern), key=extract_page_number)[:5]
    
    all_results = []
    print(f"[*] Menjalankan MODE DEBUG pada {len(pdf_files)} halaman pertama...")

    for f in pdf_files:
        try:
            print(f"[>] Menganalisis: {os.path.basename(f)}")
            pages = convert_from_path(f, dpi=150)
            if not pages: continue
            
            img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)
            h, w, _ = img.shape

            # ROI 1: Judul (Kanan Bawah)
            roi_footer = img[int(h*0.80):h, int(w*0.60):w]
            # ROI 2: Tabel Equipment (Area Atas - diperluas hingga 40% tinggi)
            roi_header = img[0:int(h*0.40), 0:w]

            # SIMPAN GAMBAR ROI (Hanya untuk halaman pertama) untuk cek visual
            if extract_page_number(f) == 1:
                cv2.imwrite("data/output/debug_roi_tabel.png", roi_header)
                print("[!] Gambar area tabel disimpan di data/output/debug_roi_tabel.png. Silakan cek apakah tabelnya terlihat!")

            # Proses OCR
            footer_pred = ocr_engine.predict(roi_footer)
            header_pred = ocr_engine.predict(roi_header)

            page_title = " ".join(get_text_from_prediction(footer_pred))
            header_texts = get_text_from_prediction(header_pred)

            if not header_texts:
                print(f"    [?] Tidak ada teks terdeteksi di area tabel halaman {extract_page_number(f)}")

            for text in header_texts:
                # Kita ambil SEMUA teks yang terbaca di area tabel tanpa filter regex dulu
                all_results.append({
                    "Halaman": extract_page_number(f),
                    "Judul P&ID": page_title.strip(),
                    "Teks Terbaca": text.strip()
                })

            del img
            gc.collect()

        except Exception as e:
            print(f"[ERROR] {f}: {e}")

    if all_results:
        df = pd.DataFrame(all_results)
        df.to_excel(output_file, index=False)
        print(f"\n[SUCCESS] Selesai! Cek file: {output_file}")
    else:
        print("\n[!] BENAR-BENAR TIDAK ADA DATA. Cek apakah folder input benar.")

if __name__ == "__main__":
    os.makedirs("data/output", exist_ok=True)
    main()