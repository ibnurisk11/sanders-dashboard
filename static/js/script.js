// static/js/script.js

// Perhatikan, default Django berjalan di port 8000
const API_BASE_URL = 'http://127.0.0.1:8000';
let currentPageUsers = 1;
let totalPagesUsers = 1;
let currentLimitUsers = 10;

let currentPageLoans = 1;
let totalPagesLoans = 1;
let currentLimitLoans = 10;

// Fungsi untuk membuka/menutup sidebar
function toggleSidebar() {
    const wrapper = document.getElementById('wrapper');
    wrapper.classList.toggle('toggled');
}

function showSection(sectionId, event) { // Tambahkan parameter event
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.add('hidden'); // Use Tailwind's hidden class
    });
    document.getElementById(sectionId).classList.remove('hidden'); // Remove hidden class

    document.querySelectorAll('.list-group-item').forEach(item => {
        // Remove Tailwind active classes
        item.classList.remove('bg-blue-600', 'text-white', 'font-bold');
        // Re-add default Tailwind inactive classes
        item.classList.add('bg-transparent', 'text-gray-400');
    });

    // Menggunakan event.target untuk mendapatkan elemen yang diklik
    // Jika event null (misal dipanggil dari DOMContentLoaded), cari elemen secara manual
    const clickedItem = event && event.target ? event.target : document.querySelector(`.list-group-item[onclick*="${sectionId}"]`);
    if (clickedItem) {
        // Add Tailwind active classes
        clickedItem.classList.add('bg-blue-600', 'text-white', 'font-bold');
        // Remove default Tailwind inactive classes
        clickedItem.classList.remove('bg-transparent', 'text-gray-400');
    }

    if (sectionId === 'borrowerListSection') {
        fetchUsers(currentPageUsers);
    } else if (sectionId === 'loanListSection') {
        fetchLoans(currentPageLoans);
    }
    // Tambahkan pemanggilan fetch untuk section lain di sini jika ada
    // else if (sectionId === 'outstandingListSection') {
    //     fetchOutstanding(currentPageOutstanding);
    // }
    // ... dst
}

function changePage(direction) {
    const newPage = currentPageUsers + direction;
    if (newPage >= 1 && newPage <= totalPagesUsers) {
        currentPageUsers = newPage;
        fetchUsers(currentPageUsers);
    }
}

function changeLoanPage(direction) {
    const newPage = currentPageLoans + direction;
    if (newPage >= 1 && newPage <= totalPagesLoans) {
        currentPageLoans = newPage;
        fetchLoans(currentPageLoans);
    }
}

document.getElementById('limitSelect').addEventListener('change', (event) => {
    currentLimitUsers = parseInt(event.target.value);
    currentPageUsers = 1;
    fetchUsers(currentPageUsers);
});

document.getElementById('loanLimitSelect').addEventListener('change', (event) => {
    currentLimitLoans = parseInt(event.target.value);
    currentPageLoans = 1;
    fetchLoans(currentPageLoans);
});

// Fungsi pembantu untuk memformat mata uang
function formatCurrency(amount) {
    if (typeof amount !== 'number' && typeof amount !== 'string') return 'N/A';
    const num = parseFloat(amount);
    if (isNaN(num)) return 'N/A';
    return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(num);
}

// Fungsi pembantu untuk memformat tanggal
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('id-ID');
    } catch (e) {
        console.error('Invalid date string:', dateString, e);
        return 'N/A';
    }
}

// Fungsi pembantu untuk memformat waktu (jika masih diperlukan)
function formatTime(timeString) {
    if (!timeString) return 'N/A';
    try {
        const date = new Date(timeString);
        return date.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
    } catch (e) {
        console.error('Invalid time string:', timeString, e);
        return 'N/A';
    }
}


async function fetchUsers(pageToFetch = currentPageUsers) {
    const filterCode = document.getElementById('filterRegisterCode').value;
    const filterFullname = document.getElementById('filterBioFullname').value;
    const filterStatus = document.getElementById('filterActivationStatus').value;
    currentLimitUsers = parseInt(document.getElementById('limitSelect').value);

    let url = new URL(`${API_BASE_URL}/users/`); // Tambahkan slash di akhir untuk URL Django
    url.searchParams.append('page', pageToFetch);
    url.searchParams.append('limit', currentLimitUsers);

    if (filterCode) {
        url.searchParams.append('register_code', filterCode);
    }
    if (filterFullname) {
        url.searchParams.append('bio_fullname', filterFullname);
    }
    if (filterStatus) {
        url.searchParams.append('activation_status', filterStatus);
    }

    try {
        const response = await fetch(url.toString());
        const data = await response.json();
        const userTableBody = document.getElementById('userTableBody');
        userTableBody.innerHTML = '';

        if (data.status === 'success' && data.data.length > 0) {
            data.data.forEach((user, index) => {
                const row = userTableBody.insertRow();
                row.className = index % 2 === 0 ? 'bg-white' : 'bg-gray-50'; // Tailwind striped rows
                row.innerHTML = `
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${user.register_code || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${user.register_email || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${user.bio_fullname || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${user.register_activation_status || 'N/A'}</td>
                `;
            });
            currentPageUsers = data.pagination.current_page;
            totalPagesUsers = data.pagination.total_pages;
            document.getElementById('pageInfo').innerText = `Halaman ${currentPageUsers} dari ${totalPagesUsers}`;
            document.getElementById('prevPageBtn').disabled = currentPageUsers === 1;
            document.getElementById('nextPageBtn').disabled = currentPageUsers === totalPagesUsers;

        } else if (data.status === 'success' && data.data.length === 0) {
            userTableBody.innerHTML = '<tr><td colspan="4" class="py-4 px-6 text-center text-gray-600">Tidak ada pengguna ditemukan.</td></tr>';
            totalPagesUsers = 1;
            currentPageUsers = 1;
            document.getElementById('pageInfo').innerText = `Halaman 1 dari 1`;
            document.getElementById('prevPageBtn').disabled = true;
            document.getElementById('nextPageBtn').disabled = true;
        } else {
            userTableBody.innerHTML = `<tr><td colspan="4" class="py-4 px-6 text-center text-red-500 font-bold">Error: ${data.message || 'Gagal mengambil data pengguna.'}</td></tr>`;
            totalPagesUsers = 1;
            currentPageUsers = 1;
            document.getElementById('pageInfo').innerText = `Halaman 1 dari 1`;
            document.getElementById('prevPageBtn').disabled = true;
            document.getElementById('nextPageBtn').disabled = true;
        }
    } catch (error) {
        console.error('Error fetching users from Django Backend:', error);
        userTableBody.innerHTML = `<tr><td colspan="4" class="py-4 px-6 text-center text-red-500 font-bold">Terjadi kesalahan saat menghubungi API Django Backend: ${error.message}</td></tr>`;
        totalPagesUsers = 1;
        currentPageUsers = 1;
        document.getElementById('pageInfo').innerText = `Halaman 1 dari 1`;
        document.getElementById('prevPageBtn').disabled = true;
        document.getElementById('nextPageBtn').disabled = true;
    }
}

async function fetchLoans(pageToFetch = currentPageLoans) {
    const filterRegisterCode = document.getElementById('filterLoanRegisterCode').value;
    const filterStatus = document.getElementById('filterLoanStatus').value;
    const filterMinAmount = document.getElementById('filterMinAmount').value;
    const filterMaxAmount = document.getElementById('filterMaxAmount').value;
    currentLimitLoans = parseInt(document.getElementById('loanLimitSelect').value);

    let url = new URL(`${API_BASE_URL}/loans/`); // Tambahkan slash di akhir untuk URL Django
    url.searchParams.append('page', pageToFetch);
    url.searchParams.append('limit', currentLimitLoans);

    if (filterRegisterCode) {
        url.searchParams.append('register_code', filterRegisterCode);
    }
    if (filterStatus) {
        url.searchParams.append('loan_status', filterStatus);
    }
    if (filterMinAmount) {
        url.searchParams.append('min_amount', filterMinAmount);
    }
    if (filterMaxAmount) {
        url.searchParams.append('max_amount', filterMaxAmount);
    }

    try {
        const response = await fetch(url.toString());
        const data = await response.json();
        const loanTableBody = document.getElementById('loanTableBody');
        loanTableBody.innerHTML = '';

        if (data.status === 'success' && data.data.length > 0) {
            data.data.forEach((loan, index) => {
                const row = loanTableBody.insertRow();
                row.className = index % 2 === 0 ? 'bg-white' : 'bg-gray-50'; // Tailwind striped rows
                row.innerHTML = `
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.register_code || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.bio_fullname || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${formatDate(loan.register_date)}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.register_email || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.virtual_account || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.id_borrower_loan || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${formatDate(loan.tanggal_pengajuan)}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.loan_type || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${formatCurrency(loan.loan_amount)}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.loan_tenor || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.loan_rate || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.loan_flat_rate || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.fee_pg || 'N/A'}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${formatDate(loan.loan_start_date)}</td>
                    <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.loan_status || 'N/A'}</td>
                `;
            });
            currentPageLoans = data.pagination.current_page;
            totalPagesLoans = data.pagination.total_pages;
            document.getElementById('loanPageInfo').innerText = `Halaman ${currentPageLoans} dari ${totalPagesLoans}`;
            document.getElementById('prevLoanPageBtn').disabled = currentPageLoans === 1;
            document.getElementById('nextLoanPageBtn').disabled = currentPageLoans === totalPagesLoans;

        } else if (data.status === 'success' && data.data.length === 0) {
            // Ubah colspan sesuai jumlah kolom baru (15 kolom)
            loanTableBody.innerHTML = '<tr><td colspan="15" class="py-4 px-6 text-center text-gray-600">Tidak ada pinjaman ditemukan.</td></tr>';
            totalPagesLoans = 1;
            currentPageLoans = 1;
            document.getElementById('loanPageInfo').innerText = `Halaman 1 dari 1`;
            document.getElementById('prevLoanPageBtn').disabled = true;
            document.getElementById('nextLoanPageBtn').disabled = true;
        } else {
            // Ubah colspan sesuai jumlah kolom baru (15 kolom)
            loanTableBody.innerHTML = `<tr><td colspan="15" class="py-4 px-6 text-center text-red-500 font-bold">Error: ${data.message || 'Gagal mengambil data pinjaman.'}</td></tr>`;
            totalPagesLoans = 1;
            currentPageLoans = 1;
            document.getElementById('loanPageInfo').innerText = `Halaman 1 dari 1`;
            document.getElementById('prevLoanPageBtn').disabled = true;
            document.getElementById('nextLoanPageBtn').disabled = true;
        }
    } catch (error) {
        console.error('Error fetching loans from Django Backend:', error);
        // Ubah colspan sesuai jumlah kolom baru (15 kolom)
        loanTableBody.innerHTML = `<tr><td colspan="15" class="py-4 px-6 text-center text-red-500 font-bold">Terjadi kesalahan saat menghubungi API Django Backend: ${error.message}</td></tr>`;
        totalPagesLoans = 1;
        currentPageLoans = 1;
        document.getElementById('loanPageInfo').innerText = `Halaman 1 dari 1`;
        document.getElementById('prevLoanPageBtn').disabled = true;
        document.getElementById('nextLoanPageBtn').disabled = true;
    }
}

async function fetchUserDetail() {
    const detailCode = document.getElementById('detailRegisterCode').value;
    if (!detailCode) {
        document.getElementById('userDetail').innerHTML = '<p class="text-red-500 font-bold">Mohon masukkan Register Code.</p>';
        return;
    }

    const url = `${API_BASE_URL}/users/${encodeURIComponent(detailCode)}/`; // Tambahkan slash di akhir untuk URL Django

    try {
        const response = await fetch(url.toString());
        const data = await response.json();

        const userDetailDiv = document.getElementById('userDetail');
        userDetailDiv.innerHTML = '';

        if (response.ok && data.status === 'success') {
            // Updated to use Tailwind classes for the detail view
            let loansHtml = '';
            if (data.data.loans && data.data.loans.length > 0) {
                loansHtml = `
                    <h4 class="text-lg font-semibold mt-6 mb-3">Daftar Pinjaman Pengguna:</h4>
                    <div class="overflow-x-auto rounded-lg shadow-sm border border-gray-300">
                        <table class="min-w-full bg-white">
                            <thead>
                                <tr class="bg-blue-600 text-white uppercase text-sm leading-normal">
                                    <th class="py-4 px-6 text-left border-b border-gray-400 whitespace-nowrap">Loan ID</th>
                                    <th class="py-4 px-6 text-left border-b border-gray-400 whitespace-nowrap">Amount</th>
                                    <th class="py-4 px-6 text-left border-b border-gray-400 whitespace-nowrap">Status</th>
                                    <th class="py-4 px-6 text-left border-b border-gray-400 whitespace-nowrap">Date</th>
                                    <th class="py-4 px-6 text-left border-b border-gray-400 whitespace-nowrap">Tenor</th>
                                    <th class="py-4 px-6 text-left border-b border-gray-400 whitespace-nowrap">Type</th>
                                </tr>
                            </thead>
                            <tbody class="text-gray-700 text-sm">
                                ${data.data.loans.map((loan, index) => `
                                    <tr class="${index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}">
                                        <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.id_borrower_loan || 'N/A'}</td>
                                        <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${formatCurrency(loan.loan_amount)}</td>
                                        <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.loan_status || 'N/A'}</td>
                                        <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${formatDate(loan.loan_date)}</td>
                                        <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.loan_tenor || 'N/A'}</td>
                                        <td class="py-4 px-6 border-b border-gray-300 whitespace-nowrap">${loan.loan_type || 'N/A'}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            } else {
                loansHtml = '<p class="text-gray-600 mt-4">Tidak ada data pinjaman untuk pengguna ini.</p>';
            }

            userDetailDiv.innerHTML = `
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <h3 class="text-xl font-bold mb-4 border-b pb-2">Detail Pengguna: ${data.data.register_code || 'N/A'}</h3>
                    <p class="mb-2"><strong class="font-semibold">Email:</strong> ${data.data.register_email || 'N/A'}</p>
                    <p class="mb-2"><strong class="font-semibold">Status Aktivasi:</strong> ${data.data.register_activation_status || 'N/A'}</p>
                    <h4 class="text-lg font-semibold mt-4 mb-3 border-b pb-1">Informasi Biografi:</h4>
                    <p class="mb-2"><strong class="font-semibold">Nama Lengkap:</strong> ${data.data.bio_fullname || 'N/A'}</p>
                    <p class="mb-2"><strong class="font-semibold">NIK:</strong> ${data.data.bio_nik || 'N/A'}</p>
                    <p class="mb-2"><strong class="font-semibold">Pekerjaan:</strong> ${data.data.bio_occupation || 'N/A'}</p>
                    <p class="mb-2"><strong class="font-semibold">Telepon:</strong> ${data.data.bio_phone || 'N/A'}</p>
                    <p class="mb-2"><strong class="font-semibold">Nama Ibu Kandung:</strong> ${data.data.bio_mother_name || 'N/A'}</p>
                    <p class="mb-2"><strong class="font-semibold">Status Pernikahan:</strong> ${data.data.bio_marriage_status || 'N/A'}</p>
                    <p class="mb-2"><strong class="font-semibold">Pendidikan Terakhir:</strong> ${data.data.bio_last_education || 'N/A'}</p>
                    <p class="mb-2"><strong class="font-semibold">Tanggal Lahir:</strong> ${formatDate(data.data.bio_birth_date)}</p>
                    <p class="mb-2"><strong class="font-semibold">Tempat Lahir:</strong> ${data.data.bio_place_birth_date || 'N/A'}</p>
                    <p class="mb-2"><strong class="font-semibold">Jenis Kelamin:</strong> ${data.data.bio_gender || 'N/A'}</p>
                    ${loansHtml}
                </div>
            `;
        } else {
            userDetailDiv.innerHTML = `<p class="text-red-500 font-bold">Error: ${data.message || 'Gagal mengambil detail pengguna.'}</p>`;
        }
    } catch (error) {
        console.error('Error fetching user detail from Django Backend:', error);
        document.getElementById('userDetail').innerHTML = `<p class="text-red-500 font-bold">Terjadi kesalahan saat menghubungi API Django Backend: ${error.message}</p>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Tampilkan bagian daftar pengguna secara default saat halaman dimuat
    showSection('borrowerListSection');

    // Menambahkan event listener untuk select limit pinjaman
    const loanLimitSelect = document.getElementById('loanLimitSelect');
    if (loanLimitSelect) {
        loanLimitSelect.addEventListener('change', (event) => {
            currentLimitLoans = parseInt(event.target.value);
            currentPageLoans = 1;
            fetchLoans(currentPageLoans);
        });
    }
});
