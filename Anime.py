import tkinter as tk
from tkinter import ttk, messagebox
import json
import requests
import os
from PIL import Image, ImageTk
from io import BytesIO
import threading
import time
from functools import lru_cache

class QuanLyAnime:
    def __init__(self):
        self.cuaSo = tk.Tk()
        self.cuaSo.title("Quản Lý Anime")
        self.cuaSo.geometry("1200x800")
        self.cuaSo.resizable(True, True)
        self.khoiTaoTepDuLieu()
        self.boNhoDemHinhAnh = {}
        self.danhSachHienThiHienTai = []
        self.boNhoDemApi = {}
        self.hienThiManHinhDangNhap()

    def khoiTaoTepDuLieu(self):
        if not os.path.exists('nguoi_dung.json'):
            nguoiDungMacDinh = {
                "admin": {
                    "mat_khau": "admin123",
                    "vai_tro": "admin",
                    "yeu_thich": []
                },
                "nguoi_dung": {
                    "mat_khau": "user123",
                    "vai_tro": "nguoi_dung",
                    "yeu_thich": []
                }
            }
            with open('nguoi_dung.json', 'w') as f:
                json.dump(nguoiDungMacDinh, f, indent=4)

        if not os.path.exists('du_lieu_anime.json'):
            with open('du_lieu_anime.json', 'w') as f:
                json.dump([], f)

    def hienThiManHinhTai(self):
        self.khungTai = ttk.Frame(self.cuaSo, style='Tai.TFrame')
        self.khungTai.place(relx=0, rely=0, relwidth=1, relheight=1)
        nhanTai = ttk.Label(self.khungTai, text="Đang tải dữ liệu...", font=('Arial', 14))
        nhanTai.place(relx=0.5, rely=0.5, anchor='center')

    def anManHinhTai(self):
        if hasattr(self, 'khungTai'):
            self.khungTai.destroy()

    def nhiemVuNen(self, nhiemVu, *doiSo):
        self.hienThiManHinhTai()
        try:
            ketQua = nhiemVu(*doiSo)
            self.cuaSo.after(0, lambda: self.nhiemVuHoanThanh(ketQua))
        except Exception as e:
            self.cuaSo.after(0, lambda: self.nhiemVuThatBai(str(e)))

    def nhiemVuHoanThanh(self, ketQua):
        self.anManHinhTai()
        if ketQua:
            self.danhSachHienThiHienTai = ketQua
            self.hienThiLuoiAnime(ketQua)

    def nhiemVuThatBai(self, thongBaoLoi):
        self.anManHinhTai()
        messagebox.showerror("Lỗi", thongBaoLoi)

    def hienThiManHinhDangNhap(self):
        for widget in self.cuaSo.winfo_children():
            widget.destroy()
        self.nhanHinhNen = tk.Label(self.cuaSo)
        self.nhanHinhNen.place(relx=0, rely=0, relwidth=1, relheight=1)
        try:
            if not os.path.exists("a2.png"):
                messagebox.showerror("Lỗi", "Không tìm thấy tệp a2.png")
                return
            self.hinhNen = Image.open("a2.png").resize((1920, 1200), Image.Resampling.LANCZOS)
            self.anhHinhNen = ImageTk.PhotoImage(self.hinhNen)
            self.nhanHinhNen.configure(image=self.anhHinhNen)
            self.nhanHinhNen.image = self.anhHinhNen
            self.nhanHinhNen.lower()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải hình nền: {str(e)}")
            return
        khungDangNhap = ttk.Frame(self.cuaSo)
        khungDangNhap.place(relx=0.5, rely=0.5, anchor='center')
        try:
            if not os.path.exists("a1.png"):
                messagebox.showerror("Lỗi", "Không tìm thấy tệp a1.png")
                return
            hinhNenKhung = Image.open("a1.png").resize((300, 200), Image.Resampling.LANCZOS)
            self.anhHinhNenKhung = ImageTk.PhotoImage(hinhNenKhung)
            nhanHinhNenKhung = tk.Label(khungDangNhap, image=self.anhHinhNenKhung)
            nhanHinhNenKhung.image = self.anhHinhNenKhung
            nhanHinhNenKhung.grid(row=0, column=0, rowspan=4, columnspan=2, sticky="nsew")
            nhanHinhNenKhung.lower()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải hình nền khung đăng nhập: {str(e)}")
            return
        ttk.Label(khungDangNhap, text="Tên người dùng:").grid(row=0, column=0, padx=5, pady=5)
        oNhapTenNguoiDung = ttk.Entry(khungDangNhap)
        oNhapTenNguoiDung.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(khungDangNhap, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
        oNhapMatKhau = ttk.Entry(khungDangNhap, show="*")
        oNhapMatKhau.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(khungDangNhap, text="Đăng nhập",
                   command=lambda: self.dangNhap(oNhapTenNguoiDung.get(), oNhapMatKhau.get())
                   ).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(khungDangNhap, text="Đăng ký",
                   command=self.hienThiManHinhDangKy
                   ).grid(row=3, column=0, columnspan=2)

    def hienThiManHinhDangKy(self):
        for widget in self.cuaSo.winfo_children():
            widget.destroy()
        self.nhanHinhNen = tk.Label(self.cuaSo)
        self.nhanHinhNen.place(relx=0, rely=0, relwidth=1, relheight=1)
        try:
            if not os.path.exists("a2.png"):
                messagebox.showerror("Lỗi", "Không tìm thấy tệp a2.png")
                return
            self.hinhNen = Image.open("a2.png").resize((1570, 900), Image.Resampling.LANCZOS)
            self.anhHinhNen = ImageTk.PhotoImage(self.hinhNen)
            self.nhanHinhNen.configure(image=self.anhHinhNen)
            self.nhanHinhNen.image = self.anhHinhNen
            self.nhanHinhNen.lower()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải hình nền: {str(e)}")
            return
        khungDangKy = ttk.Frame(self.cuaSo)
        khungDangKy.place(relx=0.5, rely=0.5, anchor='center')
        try:
            if not os.path.exists("a1.png"):
                messagebox.showerror("Lỗi", "Không tìm thấy tệp a1.png")
                return
            hinhNenKhungDangKy = Image.open("a1.png").resize((300, 250), Image.Resampling.LANCZOS)
            self.anhHinhNenKhungDangKy = ImageTk.PhotoImage(hinhNenKhungDangKy)
            nhanHinhNenKhungDangKy = tk.Label(khungDangKy, image=self.anhHinhNenKhungDangKy)
            nhanHinhNenKhungDangKy.image = self.anhHinhNenKhungDangKy
            nhanHinhNenKhungDangKy.grid(row=0, column=0, rowspan=5, columnspan=2, sticky="nsew")
            nhanHinhNenKhungDangKy.lower()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải hình nền khung đăng ký: {str(e)}")
            return
        ttk.Label(khungDangKy, text="Tên người dùng:").grid(row=0, column=0, padx=5, pady=5)
        oNhapTenNguoiDung = ttk.Entry(khungDangKy)
        oNhapTenNguoiDung.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(khungDangKy, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
        oNhapMatKhau = ttk.Entry(khungDangKy, show="*")
        oNhapMatKhau.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(khungDangKy, text="Xác nhận mật khẩu:").grid(row=2, column=0, padx=5, pady=5)
        oNhapXacNhanMatKhau = ttk.Entry(khungDangKy, show="*")
        oNhapXacNhanMatKhau.grid(row=2, column=1, padx=5, pady=5)

        def dangKy():
            tenNguoiDung = oNhapTenNguoiDung.get()
            matKhau = oNhapMatKhau.get()
            xacNhanMatKhau = oNhapXacNhanMatKhau.get()
            if not tenNguoiDung or not matKhau or not xacNhanMatKhau:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ các trường")
                return
            if matKhau != xacNhanMatKhau:
                messagebox.showerror("Lỗi", "Mật khẩu không khớp")
                return
            with open('nguoi_dung.json', 'r') as f:
                nguoiDung = json.load(f)
            if tenNguoiDung in nguoiDung:
                messagebox.showerror("Lỗi", "Tên người dùng đã tồn tại")
                return
            nguoiDung[tenNguoiDung] = {
                "mat_khau": matKhau,
                "vai_tro": "nguoi_dung",
                "yeu_thich": []
            }
            with open('nguoi_dung.json', 'w') as f:
                json.dump(nguoiDung, f, indent=4)
            messagebox.showinfo("Thành công", "Đăng ký thành công!")
            self.hienThiManHinhDangNhap()

        ttk.Button(khungDangKy, text="Đăng ký",
                   command=dangKy
                   ).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(khungDangKy, text="Quay lại đăng nhập",
                   command=self.hienThiManHinhDangNhap
                   ).grid(row=4, column=0, columnspan=2)

    def dangNhap(self, tenNguoiDung, matKhau):
        with open('nguoi_dung.json', 'r') as f:
            nguoiDung = json.load(f)
        if tenNguoiDung in nguoiDung and nguoiDung[tenNguoiDung]["mat_khau"] == matKhau:
            self.nguoiDungHienTai = tenNguoiDung
            self.vaiTroHienTai = nguoiDung[tenNguoiDung]["vai_tro"]
            self.danhSachYeuThichNguoiDungHienTai = nguoiDung[tenNguoiDung].get("yeu_thich", [])
            self.hienThiManHinhChinh()
            threading.Thread(target=lambda: self.nhiemVuNen(self.layTopAnime)).start()
        else:
            messagebox.showerror("Lỗi", "Tên người dùng hoặc mật khẩu không đúng")

    def hienThiManHinhChinh(self):
        self.laCheDoYeuThich = False
        khungChinh = ttk.Frame(self.cuaSo)
        khungChinh.pack(expand=True, fill='both', padx=10, pady=10)
        khungTimKiem = ttk.Frame(khungChinh)
        khungTimKiem.pack(fill='x', pady=5)
        ttk.Label(khungTimKiem, text="Tìm kiếm Anime:").pack(side='left', padx=5)
        self.oNhapTimKiem = ttk.Entry(khungTimKiem, width=40)
        self.oNhapTimKiem.pack(side='left', padx=5)
        self.oNhapTimKiem.bind('<Return>', lambda e: self.timKiemAnimeApi())
        ttk.Button(khungTimKiem, text="Tìm kiếm",
                   command=self.timKiemAnimeApi
                   ).pack(side='left', padx=5)
        ttk.Label(khungTimKiem, text="Sắp xếp theo:").pack(side='left', padx=5)
        luaChonSapXep = ["Điểm số", "Số tập", "Tiêu đề"]
        self.bienSapXep = tk.StringVar(value="Điểm số")
        menuSapXep = ttk.OptionMenu(khungTimKiem, self.bienSapXep, "Điểm số", *luaChonSapXep,
                                    command=lambda _: self.sapXepAnime())
        menuSapXep.pack(side='left', padx=5)
        khungCheDoXem = ttk.Frame(khungChinh)
        khungCheDoXem.pack(fill='x', pady=5)
        bienCheDoXem = tk.StringVar(value="tat_ca")
        ttk.Radiobutton(khungCheDoXem, text="Tất cả Anime", variable=bienCheDoXem,
                        value="tat_ca", command=lambda: self.chuyenSangCheDoTatCa()
                        ).pack(side='left', padx=5)
        ttk.Radiobutton(khungCheDoXem, text="Yêu thích", variable=bienCheDoXem,
                        value="yeu_thich", command=self.hienThiYeuThich
                        ).pack(side='left', padx=5)
        khungNoiDung = ttk.Frame(khungChinh)
        khungNoiDung.pack(expand=True, fill='both')
        khungNoiDung.columnconfigure(0, weight=1)
        khungNoiDung.rowconfigure(0, weight=1)
        vungVe = tk.Canvas(khungNoiDung)
        thanhCuon = ttk.Scrollbar(khungNoiDung, orient="vertical", command=vungVe.yview)
        self.khungCoTheCuon = ttk.Frame(vungVe)
        self.khungCoTheCuon.columnconfigure(0, weight=1)
        self.khungCoTheCuon.bind(
            "<Configure>",
            lambda e: vungVe.configure(scrollregion=vungVe.bbox("all"))
        )
        if self.cuaSo.tk.call('tk', 'windowingsystem') == 'win32':
            vungVe.bind_all("<MouseWheel>", lambda e: vungVe.yview_scroll(int(-1*(e.delta/120)), "units"))
        else:
            vungVe.bind_all("<Button-4>", lambda e: vungVe.yview_scroll(-1, "units"))
            vungVe.bind_all("<Button-5>", lambda e: vungVe.yview_scroll(1, "units"))
        vungVe.create_window((0, 0), window=self.khungCoTheCuon, anchor="nw")
        vungVe.configure(yscrollcommand=thanhCuon.set)
        vungVe.grid(row=0, column=0, sticky="nsew")
        thanhCuon.grid(row=0, column=1, sticky="ns")
        khungNut = ttk.Frame(khungChinh)
        khungNut.pack(fill='x', pady=10)
        ttk.Button(khungNut, text="Làm mới Top Anime",
                   command=lambda: threading.Thread(target=lambda: self.nhiemVuNen(self.layTopAnime)).start()
                   ).pack(side='left', padx=5)
        ttk.Button(khungNut, text="Đăng xuất",
                   command=self.hienThiManHinhDangNhap
                   ).pack(side='right', padx=5)

    @lru_cache(maxsize=100)
    def layHinhAnh(self, url):
        try:
            phanHoi = requests.get(url)
            hinhAnh = Image.open(BytesIO(phanHoi.content))
            hinhAnh = hinhAnh.resize((200, 300), Image.Resampling.LANCZOS)
            anh = ImageTk.PhotoImage(hinhAnh)
            return anh
        except Exception:
            return None

    def layTopAnime(self):
        try:
            khoaBoNhoDem = "top_anime"
            if khoaBoNhoDem in self.boNhoDemApi:
                return self.boNhoDemApi[khoaBoNhoDem]
            time.sleep(0.5)
            phanHoi = requests.get("https://api.jikan.moe/v4/top/anime")
            if phanHoi.status_code != 200:
                raise Exception("Không thể lấy dữ liệu từ API")
            duLieuAnime = phanHoi.json()['data']
            animeDaXuLy = []
            for anime in duLieuAnime[:20]:
                animeDaXuLy.append({
                    'tieu_de': anime['title'],
                    'diem_so': str(anime.get('score', 'N/A')),
                    'so_tap': str(anime.get('episodes', 'N/A')),
                    'trang_thai': anime.get('status', 'N/A'),
                    'url_hinh_anh': anime.get('images', {}).get('jpg', {}).get('image_url', '')
                })
            self.boNhoDemApi[khoaBoNhoDem] = animeDaXuLy
            with open('du_lieu_anime.json', 'w') as f:
                json.dump(animeDaXuLy, f, indent=4)
            return animeDaXuLy
        except Exception as e:
            raise Exception(f"Không thể lấy dữ liệu anime: {str(e)}")

    def timKiemAnimeApi(self):
        truyVan = self.oNhapTimKiem.get()
        if not truyVan:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm")
            return

        def nhiemVuTimKiem():
            try:
                khoaBoNhoDem = f"tim_kiem_{truyVan}"
                if khoaBoNhoDem in self.boNhoDemApi:
                    return self.boNhoDemApi[khoaBoNhoDem]
                time.sleep(0.5)
                phanHoi = requests.get(f"https://api.jikan.moe/v4/anime", params={'q': truyVan})
                if phanHoi.status_code != 200:
                    raise Exception("Không thể lấy dữ liệu từ API")
                duLieuAnime = phanHoi.json()['data']
                if not duLieuAnime:
                    return []
                animeDaXuLy = []
                for anime in duLieuAnime[:20]:
                    animeDaXuLy.append({
                        'tieu_de': anime['title'],
                        'diem_so': str(anime.get('score', 'N/A')),
                        'so_tap': str(anime.get('episodes', 'N/A')),
                        'trang_thai': anime.get('status', 'N/A'),
                        'url_hinh_anh': anime.get('images', {}).get('jpg', {}).get('image_url', '')
                    })
                self.boNhoDemApi[khoaBoNhoDem] = animeDaXuLy
                return animeDaXuLy
            except Exception as e:
                raise Exception(f"Không thể tìm kiếm anime: {str(e)}")

        threading.Thread(target=lambda: self.nhiemVuNen(nhiemVuTimKiem)).start()

    def sapXepAnime(self):
        khoaSapXep = self.bienSapXep.get().lower()
        if khoaSapXep == "tiêu đề":
            self.danhSachHienThiHienTai.sort(key=lambda x: x['tieu_de'])
        elif khoaSapXep == "điểm số":
            self.danhSachHienThiHienTai.sort(key=lambda x: float(x['diem_so']) if x['diem_so'] != 'N/A' else 0, reverse=True)
        elif khoaSapXep == "số tập":
            self.danhSachHienThiHienTai.sort(key=lambda x: int(x['so_tap']) if x['so_tap'] != 'N/A' else 0, reverse=True)
        self.hienThiLuoiAnime(self.danhSachHienThiHienTai)

    def hienThiLuoiAnime(self, danhSachAnime):
        for widget in self.khungCoTheCuon.winfo_children():
            widget.destroy()
        if not danhSachAnime:
            khungThongBao = ttk.Frame(self.khungCoTheCuon)
            khungThongBao.pack(expand=True, fill='both', pady=50)
            ttk.Label(khungThongBao,
                      text="Không tìm thấy anime",
                      style='TieuDe.TLabel',
                      font=('Arial', 14)).pack(expand=True)
            return
        soCotToiDa = 3
        for i in range(soCotToiDa):
            self.khungCoTheCuon.columnconfigure(i, weight=1, uniform='cot')
        hang = 0
        cot = 0
        for anime in danhSachAnime:
            khungAnime = ttk.Frame(self.khungCoTheCuon, width=350)
            khungAnime.grid(row=hang, column=cot, padx=20, pady=20, sticky="nsew")
            khungAnime.grid_propagate(False)
            khungVien = ttk.Frame(khungAnime, style='The.TFrame')
            khungVien.pack(expand=True, fill='both', padx=10, pady=10)
            urlHinhAnh = anime.get('url_hinh_anh', '')
            boChuaHinhAnh = ttk.Frame(khungVien, width=200, height=300)
            boChuaHinhAnh.pack(pady=10)
            boChuaHinhAnh.pack_propagate(False)
            if urlHinhAnh:
                ttk.Label(boChuaHinhAnh, text="Đang tải...").place(relx=0.5, rely=0.5, anchor='center')
                threading.Thread(target=self.taiHinhAnhKhongDongBo, args=(boChuaHinhAnh, urlHinhAnh)).start()
            else:
                ttk.Label(boChuaHinhAnh, text="Hình ảnh không có sẵn").place(relx=0.5, rely=0.5, anchor='center')
            nhanTieuDe = ttk.Label(khungVien, text=anime['tieu_de'],
                                   wraplength=280,
                                   style='TieuDe.TLabel',
                                   justify='center')
            nhanTieuDe.pack(pady=(10, 5))
            diemSo = anime.get('diem_so', 'N/A')
            soTap = anime.get('so_tap', 'N/A')
            khungThongTin = ttk.Frame(khungVien)
            khungThongTin.pack(pady=10, fill='x')
            ttk.Label(khungThongTin, text="Điểm số: ", style='TieuDe.TLabel').pack(side='left', padx=25)
            ttk.Label(khungThongTin, text=diemSo).pack(side='left', padx=(0, 15))
            ttk.Label(khungThongTin, text="Số tập: ", style='TieuDe.TLabel').pack(side='left', padx=5)
            ttk.Label(khungThongTin, text=soTap).pack(side='left')
            laYeuThich = anime['tieu_de'] in self.danhSachYeuThichNguoiDungHienTai
            vanBanYeuThich = "♥" if laYeuThich else "♡"
            nutYeuThich = tk.Button(
                khungVien,
                text=vanBanYeuThich,
                command=lambda a=anime: self.batTatYeuThich(a),
                relief="flat",
                font=("Arial", 12),
                fg="red" if laYeuThich else "gray",
                bg="white",
                width=2,
                height=1
            )
            nutYeuThich.pack(pady=5)
            cot += 1
            if cot >= soCotToiDa:
                cot = 0
                hang += 1

    def taiHinhAnhKhongDongBo(self, boChua, url):
        anh = self.layHinhAnh(url)
        if anh:
            self.cuaSo.after(0, lambda: self.capNhatHinhAnh(boChua, anh))

    def capNhatHinhAnh(self, boChua, anh):
        for widget in boChua.winfo_children():
            widget.destroy()
        nhanHinhAnh = ttk.Label(boChua, image=anh)
        nhanHinhAnh.image = anh
        nhanHinhAnh.place(relx=0.5, rely=0.5, anchor='center')

    def batTatYeuThich(self, anime):
        try:
            with open('nguoi_dung.json', 'r') as f:
                nguoiDung = json.load(f)
            if 'yeu_thich' not in nguoiDung[self.nguoiDungHienTai]:
                nguoiDung[self.nguoiDungHienTai]['yeu_thich'] = []
            if anime['tieu_de'] in nguoiDung[self.nguoiDungHienTai]['yeu_thich']:
                nguoiDung[self.nguoiDungHienTai]['yeu_thich'].remove(anime['tieu_de'])
            else:
                nguoiDung[self.nguoiDungHienTai]['yeu_thich'].append(anime['tieu_de'])
            with open('nguoi_dung.json', 'w') as f:
                json.dump(nguoiDung, f, indent=4)
            self.danhSachYeuThichNguoiDungHienTai = nguoiDung[self.nguoiDungHienTai]['yeu_thich']
            if getattr(self, 'laCheDoYeuThich', False):
                self.hienThiYeuThich()
            else:
                self.hienThiLuoiAnime(self.danhSachHienThiHienTai)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật danh sách yêu thích: {str(e)}")

    def hienThiYeuThich(self):
        try:
            with open('nguoi_dung.json', 'r') as f:
                nguoiDung = json.load(f)
            self.danhSachYeuThichNguoiDungHienTai = nguoiDung[self.nguoiDungHienTai].get('yeu_thich', [])
            animeYeuThich = [
                anime for anime in self.danhSachHienThiHienTai
                if anime['tieu_de'] in self.danhSachYeuThichNguoiDungHienTai
            ]
            self.laCheDoYeuThich = True
            self.hienThiLuoiAnime(animeYeuThich)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách yêu thích: {str(e)}")

    def chuyenSangCheDoTatCa(self):
        self.laCheDoYeuThich = False
        self.hienThiLuoiAnime(self.danhSachHienThiHienTai)

    def chay(self):
        kieu = ttk.Style()
        kieu.configure('The.TFrame', relief='solid', borderwidth=1)
        kieu.configure('Tai.TFrame', background='white')
        self.cuaSo.option_add('*TLabel.font', ('Arial', 10))
        kieu.configure('TieuDe.TLabel', font=('Arial', 12, 'bold'))
        self.cuaSo.mainloop()

if __name__ == "__main__":
    ungDung = QuanLyAnime()
    ungDung.chay()