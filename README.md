PetekNorm Normalizasyon Uygulaması

Bu proje, PetekNorm adlı özgün bir normalizasyon yöntemini (petek katman normalizasyonu) uygulayan bir Tkinter tabanlı masaüstü uygulamasıdır.
Veri setlerindeki sayısal sütunları 0–1 veya -1–1 aralıklarına normalleştirerek yeni sütunlar ekler.

🔹 Özgün Yöntem

PetekKatman Normalizasyonu (PetekNorm), bu projeye özel geliştirilmiş bir normalizasyon yöntemidir.
Veriyi katmanlı (petek şeklinde) parçalara ayırır ve her katmanı ayrı normalize eder, böylece daha dengeli ve katman bazlı bir ölçekleme sağlar.
Bu yöntem literatürde yaygın olarak bulunmamaktadır ve tamamen bu proje için geliştirilmiştir.



****PetekKatman Normalizasyonu (PetekNorm), verileri katmanlı bir yapı gibi ele alır. İlk katmanda tek bir değer bulunur, sonraki katmanlarda 6, 12, 18… eleman bulunur; yani altıgen (petek) şeklinde büyüyen katmanlar oluşturulur. Her katmandaki değerler min–max normalizasyonu ile ölçeklenir. Böylece veri tek bir düzlemde değil, katman katman dengeli şekilde normalize edilmiş olur.

Özetle:

Veri düz bir listeye çevrilir.

Katmanlar oluşturulur (1, 6, 12, 18…).

Her katmandaki değerler ayrı ayrı 0–1 veya -1–1 aralığına normalize edilir.

Katmanlar birleştirilerek normalize edilmiş veri elde edilir.

Avantajı: Verinin dağılımı katman bazlı dengelenir, uç değerler tek bir katmanda sınırlanır, böylece daha stabil ve anlamlı normalizasyon sağlanır.



✨ Özellikler

Excel (.xlsx, .xls) ve CSV (.csv) dosyalarını yükleme

Yüklenen verilerin ön izlemesi (ilk 100 satır)

Petek Katman Normalizasyonu algoritması ile sayısal sütunları normalize etme

Sonuçları kaydetme (Excel veya CSV olarak)

Kullanıcı dostu grafik arayüz (Tkinter + ttk)


📊 Kullanım

Dosya Yükle butonu ile Excel/CSV seçin

Normalizasyon türünü seçin (0–1 veya -1–1)

Uygula butonuna tıklayın → Normalleştirilmiş sütunlar eklenecek

Kaydet butonuyla veriyi Excel/CSV olarak dışa aktarın

🧩 Normalizasyon Mantığı

Petek Katman Normalizasyonu, verileri altıgen petek katmanlarına ayırarak her katmanda min–max normalizasyonu uygular.

İlk katmanda tek değer bulunur

Sonraki katmanlarda 6, 12, 18 … eleman bulunur

Böylece veriler daha dengeli şekilde ölçeklenir

📌 Örnek Çalışma

Girdi verisi:

X          Y

5       	10

8       	20

12	      30

Çıktı (0–1 normalize edilmiş hali):

X       Y      	X_PN	       Y_PN

5     	10     	0.00	       0.00

8	      20     	0.37	       0.50

12     	30    	1.00	       1.00
