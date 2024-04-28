import os
import requests
from urllib.parse import urljoin, urlparse

def renkli_metin(yazi):
    renkler = [
        '\033[31m',  # Kırmızı
        '\033[32m',  # Yeşil
        '\033[33m',  # Sarı
        '\033[34m',  # Mavi
        '\033[35m',  # Magenta
        '\033[36m',  # Cyan
    ]
    son_efekt = '\033[0m'  # Biçimlendirmeyi sıfırla

    kelimeler = yazi.split()
    renkli_metin = ""
    for i, kelime in enumerate(kelimeler):
        renkli_metin += renkler[i % len(renkler)] + kelime + " "
    renkli_metin += son_efekt
    return renkli_metin

def dosya_indir(url, klasor=None):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            dosya_yolu = os.path.join(klasor, parsed_url.path.strip("/").split("/")[-1])  # Dosya adını al
            os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)
            with open(dosya_yolu, "wb") as f:
                f.write(response.content)
            print(f"{dosya_yolu} dosyası başarıyla indirildi.")
        else:
            print("Hata: Dosya bulunamadı veya erişilemedi.")
    except Exception as e:
        print("Hata:", e)

def tum_dosyalari_indir(url, klasor=None):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            html = response.text
            dosya_adı = os.path.join(klasor, "tum_dosyalar.html")
            with open(dosya_adı, "w", encoding="utf-8") as dosya:
                dosya.write(html)
            print(f"Tüm dosyalar {dosya_adı} adlı dosyaya kaydedildi.")
            for link in html.split('href="')[1:] + html.split('src="')[1:]:
                dosya_linki = link.split('"')[0]
                if dosya_linki.startswith("http"):
                    dosya_indir(dosya_linki, klasor)
                else:
                    dosya_linki = urljoin(base_url, dosya_linki)
                    dosya_indir(dosya_linki, klasor)
            print("Tüm dosyalar başarıyla indirildi.")
        else:
            print("Hata: Sayfa bulunamadı veya erişilemedi.")
    except Exception as e:
        print("Hata:", e)

if __name__ == "__main__":
    site_url = input(renkli_metin("\033[36mİndirmek istediğiniz sitenin URL'sini girin: "))
    klasor = os.path.expanduser("~/Downloads")
    tum_dosyalari_indir(site_url, klasor)
