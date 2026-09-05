# 🚀 edgetunnel 2.0 (Persian / Farsi Fork)

![پنل مدیریت](./img.png)

> 🌐 **Persian (Farsi) build** — this fork ships a Persian RTL admin panel, removes the Iran geo-restriction from the login page, adds edge caching, and is documented in [README.fa.md](README.fa.md). Upstream auto-sync is disabled so local changes are not overwritten.

[![License](https://img.shields.io/github/license/pourianorozi/edgetunnel?style=flat-square)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Group-blue?style=flat-square&logo=telegram)](https://t.me/CMLiussss)

---

## 📖 معرفی پروژه

**edgetunnel** یک راه‌حل تونل رمزگشایی مبتنی بر Cloudflare Workers/Pages است که ترافیک شبکه را به صورت کارآمد پردازش می‌کند و پنل مدیریت قوی و پیکربندی انعطاف‌پذیر نود ارائه می‌دهد.

این فورک شامل:
- پنل مدیریت کاملاً فارسی با پشتیبانی RTL
- حذف محدودیت جغرافیایی ایران از صفحه ورود
- کشینگ edge
- ابزار ساخت پنل فارسی (`tools/build_fa_panel.py`)

### ✨ ویژگی‌های اصلی

- 🛡️ پشتیبانی از پروتکل‌های VLESS و Trojan
- 📊 پنل مدیریت بصری با امکان تغییر تنظیمات زنده، مشاهده لاگ و آمار ترافیک
- 🛠️ استقرار آسان روی CF Workers و CF Pages
- 🔄 سیستم سابسکریپشن خودکار و تبدیل obfuscation
- ⚡ پشتیبانی از ProxyIP سفارشی، SOCKS5/HTTP proxy زنجیره‌ای و API بهینه
- 🌐 سازگار با Windows, Android, iOS, MacOS و نرم‌افزارهای روتر

---

## 💡 استقرار سریع

### Workers

1. یک Worker جدید در Cloudflare بسازید.
2. محتوای `_worker.js` را در ادیتور Worker قرار دهید.
3. متغیر محیطی `ADMIN` را با رمز عبور مدیر اضافه کنید.
4. یک KV Namespace با نام `KV` بایند کنید.
5. دامنه سفارشی اضافه کنید و به `/admin` بروید.

### Pages (توصیه می‌شود)

1. این ریپو را Fork کنید یا فایل‌های پروژه را zip کنید و در CF Pages آپلود کنید.
2. متغیر `ADMIN` را تنظیم کنید.
3. KV با نام `KV` بایند کنید.
4. دامنه سفارشی تنظیم کنید.

برای راهنمای کامل به [مستندات اصلی](https://cmliussss.com/p/edt2/) مراجعه کنید.

---

## 🔑 متغیرهای محیطی

| متغیر | اجباری | توضیح |
|-------|--------|------|
| **ADMIN** | ✅ | رمز عبور پنل مدیریت |
| **UUID** | ❌ | UUID ثابت (فقط v4) |
| **PROXYIP** | ❌ | آی‌پی پروکسی سراسری |
| **KEY** | ❌ | کلید مسیر سابسکریپشن سریع |

---

## 📂 ساختار پروژه

```
├── _worker.js              # Worker اصلی
├── panel/
│   ├── admin/index.html    # پنل مدیریت فارسی (RTL)
│   ├── login/index.html    # صفحه ورود فارسی
│   ├── noADMIN/            # صفحه خطا وقتی ADMIN تنظیم نشده
│   └── noKV/               # صفحه خطا وقتی KV متصل نیست
├── tools/
│   ├── build_fa_panel.py   # اسکریپت ساخت پنل فارسی
│   ├── fa_panel/fa_dict.py # دیکشنری ترجمه
│   └── upstream-panel.zip  # سورس اصلی پنل
├── README.md / README.fa.md
├── wrangler.toml
└── LICENSE
```

---

## 📄 لایسنس

GNU General Public License v2.0 — نگاه کنید به [LICENSE](LICENSE).

Upstream: [cmliu/edgetunnel](https://github.com/cmliu/edgetunnel)
