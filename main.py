# main.py

import customtkinter as ctk
from PIL import Image
import math
import os
import hashlib
import threading
import time

# --- PENCERE 1: ANİMASYONLU BAŞLANGIÇ EKRANI (SPLASH SCREEN) ---

class SplashScreen(ctk.CTkToplevel):
    """
    Program açıldığında beliren, kısa süreli bir duyuru/animasyon penceresi.
    """
    def __init__(self, parent):
        super().__init__(parent)

        # Pencere ayarları
        self.geometry("400x250")
        self.title("Yükleniyor...")
        self.overrideredirect(True) # Pencere kenarlıklarını kaldırarak modern bir görünüm sağlar.

        # Pencereyi ana uygulamanın ortasında konumlandır
        parent.update_idletasks() # Ana pencerenin boyutlarını doğru almak için
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        self.geometry(f"+{parent_x + parent_width // 2 - 200}+{parent_y + parent_height // 2 - 125}")

        # Logo (logo.png dosyasının aynı klasörde olduğundan emin olun)
        try:
            logo_image = ctk.CTkImage(Image.open("logo.png"), size=(120, 120))
            logo_label = ctk.CTkLabel(self, image=logo_image, text="")
            logo_label.pack(pady=(20, 10))
        except FileNotFoundError:
            logo_label = ctk.CTkLabel(self, text="[Logo Bulunamadı]", font=ctk.CTkFont(size=14))
            logo_label.pack(pady=(60, 10))


        self.info_label = ctk.CTkLabel(self, text="Antivirüs Başlatılıyor...", font=ctk.CTkFont(size=16, weight="bold"))
        self.info_label.pack(pady=10)

        # Yükleme çubuğu animasyonu
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode='indeterminate')
        self.progressbar.pack(pady=(0, 20), padx=30, fill="x")
        self.progressbar.start()

        # 3 saniye sonra ana pencereyi göster ve bu ekranı kapat
        self.after(3000, self.close_splash)

    def close_splash(self):
        self.progressbar.stop()
        self.master.deiconify() # Ana pencereyi göster
        self.destroy() # Başlangıç ekranını kapat


# --- PENCERE 2: TARAMA SONUÇLARI VE ONAY PENCERESİ ---

class ResultsWindow(ctk.CTkToplevel):
    """
    Tespit edilen virüslerin listelendiği ve temizleme onayı istenen pencere.
    """
    def __init__(self, parent, virus_list):
        super().__init__(parent)
        self.virus_list = virus_list
        self.parent = parent # Ana pencereye erişim için
        
        self.title("Tehditler Bulundu!")
        self.geometry("700x400")
        self.grab_set() # Bu pencere açıkken ana pencereye tıklamayı engelle
        self.protocol("WM_DELETE_WINDOW", self.destroy) # Pencere kapatıldığında grab_set'i kaldır

        main_label = ctk.CTkLabel(self, text="Aşağıdaki tehditler tespit edildi:", font=ctk.CTkFont(size=18, weight="bold"))
        main_label.pack(pady=10)
        
        # Tespit Edilen Dosyalar için Kaydırılabilir Çerçeve
        scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Tespit Edilen Dosyalar")
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Bulunan virüsleri listele
        if not self.virus_list:
            label = ctk.CTkLabel(scrollable_frame, text="Tarama tamamlandı. Tehdit bulunamadı.")
            label.pack(pady=20, padx=10)
        else:
            for virus in self.virus_list:
                file_info = f"Dosya: {virus['path']}\nTehdit: {virus['virus']}"
                label = ctk.CTkLabel(scrollable_frame, text=file_info, justify="left", font=ctk.CTkFont(size=13))
                label.pack(pady=5, padx=10, anchor="w")
            
        # Butonlar
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)
        
        clean_button = ctk.CTkButton(button_frame, text="Tümünü Temizle", command=self.clean_files, fg_color="red", hover_color="#C40000")
        clean_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="İptal", command=self.destroy, fg_color="gray", hover_color="#555555")
        cancel_button.pack(side="left", padx=10)

    def clean_files(self):
        print("Temizleme işlemi başlatıldı...")
        # GERÇEK KARANTİNA VEYA SİLME İŞLEMİ BURADA YAPILIR
        # Bu örnekte sadece konsola yazdırıyoruz.
        for virus in self.virus_list:
            print(f"'{virus['path']}' dosyası karantinaya alınıyor...")
        
        # İşlem sonrası ana pencereyi bilgilendir ve güncelle
        self.parent.on_scan_completed(len(self.virus_list), cleaned=True)
        self.destroy()


# --- ANA UYGULAMA PENCERESİ ---

class AntivirusApp(ctk.CTk):
    """
    Ana Kontrol Paneli: Sağlık göstergesi ve tarama butonlarının bulunduğu ana arayüz.
    """
    def __init__(self):
        super().__init__()
        self.title("REV1NT")
        self.geometry("850x550")
        self.withdraw() # Ana pencereyi başlangıçta gizle

        # Başlangıç ekranını oluştur ve göster
        splash = SplashScreen(self)
        
        # --- Sol Panel: Gösterge ve Durum ---
        left_frame = ctk.CTkFrame(self, width=300)
        left_frame.pack(side="left", fill="y", padx=20, pady=20)

        health_label = ctk.CTkLabel(left_frame, text="Bilgisayar Sağlığı", font=ctk.CTkFont(size=20, weight="bold"))
        health_label.pack(pady=(20, 10))

        # Sağlık Göstergesi (Canvas ile çizilir)
        self.health_canvas = ctk.CTkCanvas(left_frame, width=250, height=150, bg="#2b2b2b", highlightthickness=0)
        self.health_canvas.pack(pady=20)
        self.draw_gauge(100) # Başlangıçta %100 sağlıklı

        self.status_label = ctk.CTkLabel(left_frame, text="Durum: Güvende", font=ctk.CTkFont(size=16))
        self.status_label.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(left_frame, orientation="horizontal")
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0) # Başlangıçta gizli
        self.progress_bar.pack_forget()

        # --- Sağ Panel: Tarama Seçenekleri ---
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(self.right_frame, text="Tarama Seçenekleri", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)

        self.simple_scan_btn = ctk.CTkButton(self.right_frame, text="Basit Tarama", height=50, font=ctk.CTkFont(size=16), command=lambda: self.start_scan("simple"))
        self.simple_scan_btn.pack(fill="x", padx=50, pady=10)

        self.medium_scan_btn = ctk.CTkButton(self.right_frame, text="Orta Düzey Tarama", height=50, font=ctk.CTkFont(size=16), command=lambda: self.start_scan("medium"))
        self.medium_scan_btn.pack(fill="x", padx=50, pady=10)

        self.hard_scan_btn = ctk.CTkButton(self.right_frame, text="Derin Tarama", height=50, font=ctk.CTkFont(size=16), command=lambda: self.start_scan("hard"))
        self.hard_scan_btn.pack(fill="x", padx=50, pady=10)

    def draw_gauge(self, percentage):
        """Sağlık göstergesini (hız kadranı) çizen fonksiyon."""
        self.health_canvas.delete("all")
        width = 250
        height = 150
        center_x, center_y, radius = width / 2, height - 20, 100

        # Renkler sağlık durumuna göre değişir
        color = "green" if percentage > 75 else "orange" if percentage > 40 else "red"

        # Arka plan yayı (gri)
        self.health_canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                                      start=0, extent=180, style="arc", outline="#424242", width=20)
        
        # Değer yayı (renkli)
        if percentage > 0:
            self.health_canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                                          start=180, extent=-(percentage * 1.8), style="arc", outline=color, width=20)

        # Yüzde metni
        self.health_canvas.create_text(center_x, center_y - 40, text=f"{int(percentage)}%", font=("Arial", 24, "bold"), fill="white")

    def start_scan(self, scan_type):
        """Tarama işlemini arayüzü kilitlemeden bir thread içinde başlatır."""
        self.set_ui_for_scanning(True)
        # Tarama işlemini arayüzün donmasını engellemek için yeni bir thread'de başlat
        scan_thread = threading.Thread(target=self.run_scan_logic, args=(scan_type,))
        scan_thread.start()

    def run_scan_logic(self, scan_type):
        """Arka planda çalışacak olan asıl tarama mantığı."""
        
        # --- ÖRNEK VİRÜS VERİTABANI (GERÇEK UYGULAMADA BU BİR DOSYADAN OKUNMALIDIR) ---
        # Bu hash'ler EICAR standart test dosyasının hash'leridir. Zararsızdır.
        # İnternetten "eicar test file" diye aratıp indirerek test edebilirsiniz.
        malware_hashes = {
            "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f": "EICAR-Test-File (not a virus)"
        }
        
        # --- TARANACAK KLASÖRLERİ BELİRLE ---
        # Gerçek uygulamada bu yollar daha dinamik olmalıdır.
        if scan_type == "simple":
            paths_to_scan = [os.path.expanduser('~\\Downloads')]
        elif scan_type == "medium":
            paths_to_scan = [os.path.expanduser('~\\Downloads'), os.path.expanduser('~\\Documents'), 'C:\\Windows\\Temp']
        else: # hard
            paths_to_scan = ['C:\\'] # DİKKAT: Bütün C sürücüsünü taramak çok uzun sürer!

        found_threats = []
        file_count = 0
        for path in paths_to_scan:
            if not os.path.exists(path): continue
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_count += 1
                    # Her 50 dosyada bir arayüzü güncelle (performans için)
                    if file_count % 50 == 0:
                        self.after(0, lambda: self.status_label.configure(text=f"Taranıyor: {file_path}"))
                    try:
                        file_hash = self.calculate_hash(file_path)
                        if file_hash in malware_hashes:
                            threat_name = malware_hashes[file_hash]
                            print(f"TEHDİT BULUNDU: {file_path} -> {threat_name}")
                            found_threats.append({"path": file_path, "virus": threat_name})
                    except Exception as e:
                        # Erişim engellendi gibi hataları atla
                        # print(f"Dosya okunamadı: {file_path}, Hata: {e}")
                        pass
        
        # Tarama bittiğinde, sonuçları ana thread'de göster
        self.after(0, self.on_scan_completed, len(found_threats), False, found_threats)


    def calculate_hash(self, file_path):
        """Bir dosyanın SHA256 hash değerini hesaplar."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def set_ui_for_scanning(self, is_scanning):
        """Tarama sırasında arayüzü ayarlar (butonları pasifleştirme vb.)."""
        if is_scanning:
            self.status_label.configure(text="Tarama başlatılıyor...")
            self.simple_scan_btn.configure(state="disabled")
            self.medium_scan_btn.configure(state="disabled")
            self.hard_scan_btn.configure(state="disabled")
            self.progress_bar.pack(pady=10, padx=20, fill="x")
            self.progress_bar.start()
        else:
            self.status_label.configure(text="Durum: Güvende")
            self.simple_scan_btn.configure(state="normal")
            self.medium_scan_btn.configure(state="normal")
            self.hard_scan_btn.configure(state="normal")
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

    def on_scan_completed(self, threat_count, cleaned, threats_list=None):
        """Tarama bittiğinde çağrılır ve arayüzü günceller."""
        self.set_ui_for_scanning(False)
        
        if cleaned:
            self.status_label.configure(text=f"{threat_count} tehdit temizlendi. Bilgisayarınız güvende.", text_color="green")
            self.draw_gauge(100)
        else:
            if threat_count > 0:
                self.status_label.configure(text=f"UYARI: {threat_count} tehdit bulundu!", text_color="red")
                self.draw_gauge(20) # Sağlığı düşür
                ResultsWindow(self, threats_list) # Onay penceresini aç
            else:
                self.status_label.configure(text="Tarama bitti. Tehdit bulunamadı.", text_color="green")
                self.draw_gauge(100)


if __name__ == "__main__":
    # Uygulama modunu ve renk temasını ayarla
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    app = AntivirusApp()
    app.mainloop()