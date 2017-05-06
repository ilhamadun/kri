# Reader ID Card Peserta

Program untuk login dan logout peserta ke venue KRI Regional 3 Tahun 2017.

### Dependency
Library yang perlu diinstall:
- [libcurl](http://curl.haxx.se/libcurl/)
- [restclient-cpp](https://github.com/mrtazz/restclient-cpp)
- **Library untuk baca USB belum ada**

### Instalasi
Build program dengan:

```shell
make
```

### Penggunaan
Jalankan program dengan:

```shell
./reader [login|logout] USERNAME PASSWORD [HOST]
```

Keterangan:
- Mode `login` atau `logout` menentukan logger masuk atau keluar ruangan
- `USERNAME` dan `PASSWORD` untuk akun admin
- `HOST` default ke https://kri2017.ugm.ac.id, bisa diganti untuk keperluan pengembangan
