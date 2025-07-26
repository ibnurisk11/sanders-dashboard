Sanders Dashboard: Panel Admin Manajemen Pengguna & Pinjaman
(Ganti placeholder ini dengan screenshot asli dari dashboard Anda!)

Gambaran Umum Proyek
Sanders Dashboard adalah panel administrasi backend yang kuat dan responsif, dirancang khusus untuk mengelola data pengguna (borrower) dan pinjaman dalam ekosistem perusahaan fintech Sanders. Dibangun dengan Django untuk backend yang kokoh dan Tailwind CSS untuk antarmuka pengguna yang modern dan adaptif, dashboard ini menyediakan alat yang efisien untuk pemantauan dan manajemen operasional.

Fitur Utama
Daftar Borrower Komprehensif: Lihat daftar lengkap pengguna (borrower) dengan kemampuan filter berdasarkan kode register, nama lengkap, dan status aktivasi.

Daftar Pinjaman Detail: Akses daftar pinjaman dengan informasi terperinci, termasuk tanggal pengajuan, jenis pinjaman, jumlah, tenor, suku bunga, dan status. Dilengkapi dengan filter berdasarkan kode register peminjam, status pinjaman, serta rentang jumlah pinjaman (min/max).

Detail Pengguna Lengkap: Dapatkan tampilan mendalam tentang setiap pengguna, termasuk informasi biografi (NIK, pekerjaan, kontak, dll.) dan riwayat pinjaman terkait.

Pagination Efisien: Navigasi data dalam jumlah besar dengan mudah berkat sistem pagination yang terimplementasi.

Desain Responsif: Antarmuka yang dioptimalkan untuk berbagai ukuran layar, dari desktop hingga perangkat seluler, berkat utilitas Tailwind CSS.

Sidebar Navigasi Dinamis: Sidebar yang dapat di-toggle untuk pengalaman pengguna yang lebih fleksibel, terutama pada layar kecil.

Teknologi yang Digunakan
Backend: Python (Django Framework)

Frontend: HTML, JavaScript

Styling: Tailwind CSS (via CDN)

Database: (Sebutkan database yang Anda gunakan, misal: PostgreSQL, MySQL, SQLite)

Cara Menjalankan Proyek (Lokal)
Untuk menjalankan proyek ini di lingkungan lokal Anda, ikuti langkah-langkah berikut:

Clone Repositori:

git clone https://github.com/YourUsername/sanders-admin-dashboard.git
cd sanders-admin-dashboard

(Ganti YourUsername dan sanders-admin-dashboard dengan detail repositori Anda)

Buat dan Aktifkan Virtual Environment (Opsional tapi Disarankan):

python -m venv venv
# Di Windows
.\venv\Scripts\activate
# Di macOS/Linux
source venv/bin/activate

Instal Dependensi Python:

pip install -r requirements.txt

(Pastikan Anda memiliki file requirements.txt yang berisi Django dan dependensi lainnya)

Konfigurasi Database:
Edit settings.py di proyek Django Anda untuk mengonfigurasi pengaturan database Anda.

Jalankan Migrasi Database:

python manage.py makemigrations core_dashboard
python manage.py migrate

Buat Superuser (untuk akses admin):

python manage.py createsuperuser

Ikuti petunjuk di layar untuk membuat akun admin.

Jalankan Server Pengembangan:

python manage.py runserver

Akses Dashboard:
Buka browser Anda dan kunjungi http://127.0.0.1:8000/. Anda akan diarahkan ke halaman login.