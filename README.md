# 🏦 Illusion PIN Banking — Advanced Authentication for Next-Gen Online Finance

A secure online banking web application built with **Python Flask** and **MySQL**, featuring Illusion PIN and Brightness PIN authentication to prevent shoulder surfing and unauthorized access.

---

## 🔐 Key Features

- **Illusion PIN Login** — Randomized keypad layout every login attempt to prevent shoulder surfing
- **Brightness PIN Login** — PIN entry using brightness levels for additional security
- **Face Recognition** — Live face detection during login for multi-factor authentication
- **OTP Verification** — Reversed OTP sent via Email & SMS for extra login security
- **Admin Dashboard** — Approve/reject new user registrations
- **User Dashboard** — View balance, transaction history, beneficiaries
- **Fund Transfer** — Secure money transfer to registered beneficiaries
- **Deposit & Withdrawal** — With SHA-256 blockchain-style transaction chaining
- **Forgot Password** — OTP-based password reset via email

---

## 🛠️ Technologies Used

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | MySQL |
| Security | SHA-256 Hashing, Face Recognition (fsdk), OTP |
| Email | SMTP (Gmail) |
| SMS | REST API |

---

## 📁 Project Structure

```
illusion-pin-banking/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── templates/              # HTML pages
│   ├── index.html
│   ├── AdminLogin.html
│   ├── AdminHome.html
│   ├── UserLogin.html
│   ├── UserHome.html
│   ├── NewUser.html
│   ├── NewPin.html
│   ├── SelectLogin.html
│   ├── LoginPin.html
│   ├── BrightnessPin.html
│   ├── OTP.html
│   ├── Transaction.html
│   ├── Deposit.html
│   ├── Withdraw.html
│   ├── TransactionInfo.html
│   ├── NewBeneficiary.html
│   ├── MulitiUser.html
│   └── ForgotPassword.html
│
└── static/                 # CSS, JS, Images
    ├── css/
    ├── js/
    └── images/             # PIN digit images (0.png - 9.png)
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/illusion-pin-banking.git
cd illusion-pin-banking
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup MySQL Database
- Create a database named `facebankingdbda`
- Create the required tables: `regtb`, `multitb`, `transtb`, `beneficiarytb`, `temptb`

### 4. Run the Application
```bash
python app.py
```

### 5. Open in Browser
```
http://localhost:5000
```

---

## 👩‍💻 Developer

**Annalakshmi S**
- 📧 annalakshmi3012@gmail.com
- 🎓 B.E. Computer Science & Engineering
- 🏫 Pavendar Bharathidasan College of Engineering and Technology, Trichy

---

## 📌 Note

This project was developed as a final year academic project focused on enhancing banking security through innovative PIN authentication methods.
