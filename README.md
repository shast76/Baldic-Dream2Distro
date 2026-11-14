# Baldic Dream2Distro

**Sürüm 1.5.2** · Türkçe / English

Kendi Linux dağıtımınızı yapan araç. Windows ve Linux üzerinde çalışır,
Debian tabanlı bir canlı ISO'yu alıp kendi kerneliniz, uygulamalarınız,
duvar kağıtlarınız ve markanızla yeniden paketler.

**D2D** kısaltmasıyla da anılır. Proje dosyaları `.d2d` uzantısını kullanır.

---

## Ne yapar

| Özellik | Açıklama |
|---|---|
| Kendi kerneliniz | `linux-image-*.deb` kurulur, canlı ISO'nun açılış dosyaları da güncellenir. `CONFIG_ANDROID_BINDERFS` açık mı diye kontrol edilir |
| C++ uygulamaları | CMake, qmake, Meson ve Makefile tanınır; sistemin içinde derlenip `.deb` olarak kurulur |
| Sınırsız duvar kağıdı | KDE duvar kağıdı listesine eklenir, biri varsayılan seçilir |
| Açılış ekranı | Plymouth teması üretilir (logo + isteğe bağlı animasyon) |
| Önyükleme menüsü | GRUB (UEFI), isolinux (eski BIOS) ve kurulu sistemin GRUB'ı — tek resimle üçü birden |
| Giriş ekranı | SDDM arka planı |
| Başlat butonu | KDE panel menü ikonu değiştirilir |
| İkon teması | Değiştirdiğiniz ikonlar + klasör türevleri; gerisi Breeze'den gelir. İkon adları kurulu `.desktop` dosyalarından çözülür, böylece `dolphin` yerine `org.kde.dolphin` bekleyen uygulamalarda da görünür |
| GRUB teması | Ayrı sekme: canlı ön izleme üzerinde sürükle-bırak konumlandırma, 5 renk seçici, `theme.txt` üretimi, arka planın 8-bit RGB non-interlaced PNG'ye çevrilmesi |
| Ağ önyükleme (PXE) | Ayrı sekme: ProxyDHCP + TFTP + HTTP, ISO sürükle-bırak, iPXE menüsü, ağ adaptörü seçimi |
| Tek açılış girişi | Canlı oturum ve kurulum ayrı ayrı listelenmez, tek giriş açılır |
| Stok duvar kağıtları | ISO ile gelenler tek anahtarla kaldırılabilir |
| Calamares | Banner, ürün ikonu, karşılama resmi, slayt gösterisi, pencere boyutu, renkler |
| Masaüstü ortamı | KDE, GNOME, XFCE, Cinnamon, LXQt, MATE arasında değiştirme |
| Terminal | ISO'nun içinde root yetkili canlı kabuk — `apt install` / `apt purge` |
| Masaüstü kısayolları | Seçtiğiniz uygulamalar `/etc/skel/Desktop` içine konur — hem canlı oturumda hem kurulumdan sonra görünür |
| Proje dosyası | Tüm seçimler `.d2d` olarak kaydedilir, sonraki sürüm tek tıkla |
| İki dil | Arayüz Türkçe ve İngilizce. Ayarlar → Arayüz dili |

---

## Kurulum

### Hazır paketler

| Sistem | Dosya | Kurulum |
|---|---|---|
| Debian / Ubuntu | `baldic-dream2distro_1.2.0_all.deb` | `sudo apt install ./baldic-dream2distro_1.2.0_all.deb` |
| Windows | kendiniz derlersiniz | `packaging\build_exe.bat` dosyasına çift tıklayın |

`.deb` kurulduktan sonra uygulama menüsünde **Baldic Dream2Distro** olarak görünür,
terminalden `dream2distro` ile de açılır.

Windows için hazır `.exe` kutuda gelmiyor çünkü Windows'ta derlenmesi gerekiyor.
`packaging\build_exe.bat` gereken paketleri kurup `dist\Dream2Distro\` klasörünü
üretir; o klasörün tamamını kopyalayın, yalnızca `.exe` tek başına çalışmaz.
Tek dosya isterseniz `packaging/dream2distro.spec` içindeki `ONEFILE` değerini
`True` yapın.

### Kaynak koddan

### Windows

1. [Python](https://python.org) kurun — kurarken **"Add Python to PATH"** işaretli olsun.
2. `run.bat` dosyasına çift tıklayın. Gerekli paketleri kendi kurar.
3. İlk açılışta WSL yoksa **Ayarlar → WSL kur** düğmesini kullanın, sonra bilgisayarı yeniden başlatın.

### Debian / Ubuntu

```bash
sudo apt install python3-pyside6.qtquick python3-pil
./run.sh
```

veya

```bash
pip install -r requirements.txt
python3 main.py
```

---

## Nasıl çalışır

ISO'nun içine girip paket kurmak ancak gerçek bir Linux ortamında yapılabilir.
Bu yüzden:

- **Windows'ta** arayüz Windows'ta çalışır, asıl iş **WSL2** içinde yapılır.
- **Linux'ta** her şey doğrudan bilgisayarda çalışır (root yetkisi istenir).

```
 Arayüz (PySide6 + QML)
        │  JSON satırları
        ▼
 engine/d2d_builder.py   ← root olarak Linux içinde
        │
        ├─ ISO açılır (xorriso)
        ├─ Dosya sistemi açılır (unsquashfs)
        ├─ chroot: kernel, paketler, C++ derleme
        ├─ Markalama: duvar kağıdı, Plymouth, SDDM, GRUB, Calamares, ikonlar
        ├─ Yeniden sıkıştırılır (mksquashfs)
        └─ ISO yazılır (xorriso — BIOS + UEFI açılışı korunur)
```

Açılış ayarları orijinal ISO'dan `xorriso -report_el_torito as_mkisofs` ile okunur,
yani ISO yeniden `genisoimage` ile sıfırdan kurulmaz; orijinalin önyükleme sektörleri
korunur. Bu sayede `ldlinux.c32` / `isolinux.bin` hataları yaşanmaz ve yeni ISO hem
eski BIOS'lu hem UEFI'li bilgisayarlarda açılır.

**İki önemli ayrıntı:**

- **Her şey WSL'in kendi diskinde yapılır.** Sürükleyip bıraktığınız dosyalar
  (duvar kağıtları, ikonlar, `.deb`'ler, kaynak klasörleri) derleme başlarken
  `/var/tmp/d2d-work/work/inputs` içine kopyalanır. NTFS üzerinde dosya izinleri
  bozuk göründüğü ve `/mnt/c` çok yavaş olduğu için `unsquashfs`, `chmod` ve
  `chroot` adımlarının hiçbiri Windows diskine dokunmaz.
- **apt kaynakları onarılır.** Canlı ISO'ların `sources.list` dosyasında
  `deb file:/run/live/medium ...` satırı bulunur; chroot içinde bu yol olmadığı
  için apt her komutta hata verir. Araç bu satırları (deb822 `.sources`
  biçimi dahil) siler, gerçek bir depo kalmamışsa taban sistemin kod adını
  tespit edip Debian depolarını ekler.

---

## Komut satırından kullanım

Arayüz olmadan da çalışır:

```bash
sudo python3 engine/d2d_builder.py doctor --install   # gerekli araçları kur
sudo python3 engine/d2d_builder.py build proje.d2d    # ISO üret
```

---

## Gereken araçlar

Linux tarafında şunlar gerekir, arayüz bunları kendi kurar:

`xorriso` · `squashfs-tools` · `rsync` · `dosfstools` · `mtools` · `syslinux-utils` · `python3-pil`

---

## Ağ önyükleme (PXE)

**Network Boot** sekmesinden ağdaki bilgisayarları USB olmadan başlatabilirsiniz.

1. **Ağ arayüzü** — fiziksel Ethernet kartınızı seçin (WSL ve VMware adaptörleri işe yaramaz)
2. **iPXE önyükleyicileri** — hiçbir şey kendiliğinden inmez. "Boyutları sorgula" ile her dosyanın indirme boyutunu görür, istediğinizi tek tek indirirsiniz. SHA256 ile doğrulanır; internet yoksa dosyaları elle seçebilirsiniz. Yalnızca `undionly.kpxe` (BIOS) ve `ipxe.efi` (64 bit UEFI) zorunludur.
3. **ISO ekleyin** — sürükleyip bırakın; Debian live ve Ubuntu casper otomatik tanınır
4. **Başlat** — Windows bir kez yönetici onayı sorar

Servis ayrı bir süreç olarak yükseltilir; arayüz normal kullanıcı olarak kalır.

**Başlat'a bastım, hiçbir şey olmuyor**

Network Boot sekmesindeki **Kütük** kartına bakın; sebep orada yazar. En sık
nedeni iPXE dosyalarının henüz indirilmemiş olmasıdır. Windows'ta yönetici
onayı penceresi yalnızca iPXE dosyaları hazırken çıkar.

**Bilmeniz gerekenler:**

- İstemci bilgisayarlarda **Secure Boot kapalı** olmalı (iPXE imzasız)
- Kablosuz ağlarda PXE genelde çalışmaz, kablolu bağlantı gerekir
- ProxyDHCP IP dağıtmaz, ağınızdaki mevcut DHCP sunucusunu bozmaz
- Debian live imajlarında `filesystem.squashfs` diske çıkarılır (birkaç GB yer kaplar)

---

## Sorun giderme

Ayarlar sekmesindeki **Tanılama** düğmesi ortam bilgilerini Derleme sekmesindeki
kütüğe yazar ve uygulama klasörüne `tanilama.txt` olarak kaydeder. Bir sorun
bildirirken bu dosyayı eklemek en hızlı yol.

**WSL'e bağlanamıyorum**

```powershell
wsl -l -v          # dağıtım var mı, hangi sürüm
wsl --install -d Debian    # yoksa (PowerShell'i yönetici olarak açın)
```

**`TRUST_E_BAD_DIGEST` / "Dağıtım karması eşleşmiyor"**

WSL'in bilinen bir hatası, sizinle ilgili değil. Sırayla:

```powershell
wsl --update
wsl --install -d Debian --web-download
wsl --install -d Ubuntu            # hâlâ olmazsa
```

**WSL'deki dağıtımın Debian olması gerekmez.** Araç ISO'nun kendi Debian 13
dosya sistemine `chroot` ile girer; WSL yalnızca `xorriso`, `squashfs-tools` ve
`python3`'ü çalıştıran kabuktur. Ubuntu ile de aynı Debian tabanlı ISO çıkar.

Dağıtım görünüyor ama bağlanmıyorsa, içinde Python olmayabilir:

```powershell
wsl -d Debian -u root apt-get update
wsl -d Debian -u root apt-get install -y python3 python3-pil
```

Kurduktan sonra **Ayarlar → Yeniden bağla**.

**Sürüklediğim dosyalar eklenmiyor**

1.0.1'de düzeltildi. Daha eski bir sürüm kullanıyorsanız güncelleyin.

**Açılışta `(initramfs)` istemine düşüyor**

Çekirdek yükleniyor ama canlı sistem bulunamıyor demektir. İstemde şunu yazın:

```
ls -l /run/live/medium/live/
```

- Klasör boş ya da yoksa → ISO medyası hiç bulunamamış (USB yazımı veya önyükleme
  sırası sorunu).
- `filesystem.squashfs` görünüyor ama boyutu 4 GB'da kesilmişse → dosya sistemi
  eksik yazılmış. 1.2.1 bu durumu derleme sırasında yakalayıp durduruyor.

`cat /proc/cmdline` komutu da hangi önyükleme parametreleriyle gelindiğini gösterir.

**`UnicodeDecodeError: 'utf-8' codec can't decode byte ...`**

1.1'de düzeltildi. Dosya yollarında Türkçe karakter varken Windows ile WSL
arasındaki metin kodlaması uyuşmuyordu.

---

## English

The interface is available in English: **Settings → Interface language**.
Everything the app shows — tabs, drop zones, warnings and the build log's stage
names — switches with it. Package names, commands and tool output stay as they
are. The setting is remembered between sessions.

---

## Notlar ve sınırlar

- **Yalnızca canlı (live) ISO'lar** kullanılabilir. Kurulum (netinst / DVD) ISO'ları
  içinde squashfs olmadığı için çalışmaz.
- **Disk alanı:** kaynak ISO'nun yaklaşık 4 katı boş alan gerekir. 4 GB'lık bir ISO için ~16 GB.
- **4 GB'ı aşan ISO'lar:** dosya sistemi 4 GiB'ı geçerse ISO otomatik olarak
  ISO 9660 seviye 3 ile yazılır. Böyle bir ISO **FAT32 biçimli bir USB belleğe
  kopyalanamaz** — Rufus veya `dd` ile yazın. Daha küçük bir ISO için Ayarlar'dan
  `xz` sıkıştırmasını seçebilir ya da paket çıkarabilirsiniz.
- **Süre:** bilgisayara göre 15–60 dakika. `xz` sıkıştırma seçilirse daha uzun.
- **Hız:** Windows'ta çalışma klasörü WSL'in kendi diskinde tutulur
  (`/var/tmp/d2d-work`), çünkü `/mnt/c` üzerinde çalışmak çok yavaştır.
- **Markalama şu an KDE için tam.** Diğer masaüstü ortamlarında duvar kağıdı,
  ikonlar, Plymouth ve GRUB çalışır; panel ve başlat butonu çalışmaz.
- **macOS** desteklenmiyor.

---

## Dosya düzeni

```
dream2distro/
├── main.py                  arayüzü başlatır
├── run.bat / run.sh         tek tıkla başlatıcılar
├── d2d/
│   ├── engine.py            WSL / yerel Linux bağlantısı, yol dönüşümü
│   ├── grub_bridge.py       GRUB sekmesinin hesaplama köprüsü (durum tutmaz)
│   └── netboot/             ağ önyükleme (PXE) — izole paket
│       ├── images.py        imaj kitaplığı, ISO tanıma, xorriso ile çıkarma
│       ├── menu.py          iPXE menüsü, arka plan ve renk ayarları
│       ├── service.py       ProxyDHCP + TFTP (blksize) + HTTP (Range)
│       ├── ipxe.py          iPXE indirici (SHA256) ve elle dosya seçimi
│       ├── elevate.py       yönetici yetkisi ve güvenlik duvarı kuralları
│       ├── runner.py        servisi çalıştıran ayrı süreç
│       └── bridge.py        QML köprüsü
│   ├── project.py           .d2d proje modeli, dosya alanları, doğrulama
│   └── bridge.py            QML ile Python arasındaki köprü
├── engine/
│   ├── d2d_builder.py       asıl derleme motoru (Linux içinde root)
│   ├── d2d_grub_theme.py    GRUB tema üreteci (saf Python, iki taraf da kullanır)
│   └── test_branding.py     markalama testi
├── qml/
│   ├── Main.qml             pencere, kenar çubuğu, bildirimler
│   └── D2D/                 bileşenler, sayfalar ve Tr.qml (çeviriler)
├── assets/                  logolar ve uygulama ikonu
├── packaging/
│   ├── build_deb.sh         Debian paketi üretir
│   ├── build_exe.bat        Windows .exe üretir
│   └── dream2distro.spec    PyInstaller tanımı
└── tools/
    ├── qmlcheck.py           QML denetleyici
    ├── test_integration.py   motor protokolü testleri
    ├── test_sources_skel.py  apt kaynakları ve /etc/skel testleri
    ├── test_bridge.py        arayüz köprüsü testleri
    ├── test_i18n.py          çeviri bütünlüğü testleri
    ├── test_encoding.py      Türkçe karakterli yol testleri
    ├── test_iso.py           ISO yazma testleri
    ├── test_paths.py         paketleme yolu testleri
    ├── test_squashfs.py      sıkıştırma doğrulama testleri
    ├── test_features.py      ikon adı çözümleme ve menü testleri
    ├── test_grub_theme.py    GRUB tema üreteci testleri
    ├── test_grub_bridge.py   GRUB köprüsü testleri
    ├── test_navigation.py    sekme ve sayfa tutarlılığı testleri
    ├── test_netboot_images.py  ağ önyükleme imaj kitaplığı testleri
    ├── test_netboot_menu.py    iPXE menü üretimi testleri
    ├── test_netboot_service.py ProxyDHCP / TFTP / HTTP testleri
    ├── test_netboot_ipxe.py  iPXE indirici ve servis süreci testleri
    └── test_netboot_bridge.py  ağ önyükleme köprüsü testleri
```

---

## Testler

```bash
python3 engine/test_branding.py     # 37 kontrol - markalama dosyaları
python3 tools/test_integration.py   # 50 kontrol - protokol, proje, yollar
python3 tools/test_sources_skel.py  # 22 kontrol - apt kaynakları, /etc/skel
python3 tools/test_bridge.py        # 21 kontrol - QUrl dönüşümü, WSL algılama
python3 tools/test_i18n.py          # 18 kontrol - çeviri bütünlüğü
python3 tools/test_encoding.py      #  9 kontrol - Türkçe karakterli yollar
python3 tools/test_iso.py           # 14 kontrol - birim etiketi, 4 GiB sınırı
python3 tools/test_paths.py         # 12 kontrol - paketlenmiş .exe yolları
python3 tools/test_squashfs.py      # 16 kontrol - sıkıştırma ve doğrulama
python3 tools/test_features.py      # 27 kontrol - ikon adları, menü, duvar kağıtları
python3 tools/test_grub_theme.py    # 112 kontrol - theme.txt, PNG dönüşümü, 9 parça
python3 tools/test_grub_bridge.py   # 45 kontrol - GRUB köprüsü
python3 tools/test_navigation.py    # 35 kontrol - sekme/sayfa tutarlılığı
python3 tools/test_netboot_images.py # 97 kontrol - imaj kitaplığı ve ISO tanıma
python3 tools/test_netboot_menu.py  # 88 kontrol - iPXE menü üretimi
python3 tools/test_netboot_service.py # 111 kontrol - ProxyDHCP, TFTP, HTTP
python3 tools/test_netboot_ipxe.py  # 78 kontrol - iPXE indirici, boyut sorgulama
python3 tools/test_netboot_bridge.py # 49 kontrol - ağ önyükleme köprüsü
python3 tools/qmlcheck.py           # 18 QML dosyası
```

---

## Uygulama ikonu

`assets/icon.png` şu an BD2D yazı logosundan üretildi. Küçük boyutlarda daha net
okunması için sadece 3B "2" rakamından oluşan bir sürüm hazırlayıp bu dosyanın
üzerine yazabilirsiniz (512×512 PNG önerilir).

---

## Lisans

Açık kaynak. Baldic OS ve Baldic Download Manager ile aynı aileden.
