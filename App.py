from flask import Flask, render_template, flash, request, session, redirect, url_for
import sys, math, ctypes, time
import mysql.connector
import hmac, hashlib, binascii, random, datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SECRET_KEY'] = 'illusion_pin_secret_key'


# ─────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────

def get_db():
    return mysql.connector.connect(
        user='root', password='', host='localhost', database='facebankingdbda'
    )

def remove(string):
    return string.replace(",", "")

def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()

def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms"
        "&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + " Sent By FSMSG FSSMSS"
    )


# ─────────────────────────────────────────────
# Page Routes
# ─────────────────────────────────────────────

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')

@app.route('/UserLogin', methods=['GET', 'POST'])
def UserLogin():
    return render_template('UserLogin.html')

@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')

@app.route("/ForgotPassword")
def ForgotPassword():
    return render_template('ForgotPassword1.html')

@app.route("/NewBeneficiary")
def NewBeneficiary():
    return render_template('NewBeneficiary.html')

@app.route("/Deposit")
def Deposit():
    return render_template('Deposit.html')

@app.route("/Withdraw")
def Withdraw():
    return render_template('Withdraw.html')

@app.route("/JoinUser")
def JoinUser():
    return render_template('MulitiUser.html')


# ─────────────────────────────────────────────
# Admin Routes
# ─────────────────────────────────────────────

@app.route("/AdminHome")
def AdminHome():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb WHERE status='waiting'")
    data = cur.fetchall()

    cur.execute("SELECT * FROM regtb WHERE status='Active'")
    data1 = cur.fetchall()
    conn.close()
    return render_template('AdminHome.html', data=data, data1=data1)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['Password'] == 'admin':
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb WHERE status='waiting'")
            data = cur.fetchall()
            cur.execute("SELECT * FROM regtb WHERE status='Active'")
            data1 = cur.fetchall()
            conn.close()
            flash("Admin Login Successfully")
            return render_template('AdminHome.html', data=data, data1=data1)
        else:
            flash("UserName or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/Approved")
def Approved():
    import LiveRecognition as liv
    liv.att()
    del sys.modules["LiveRecognition"]

    id = request.args.get('lid')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE regtb SET Status='Active' WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return Approved1()


@app.route("/Approved1")
def Approved1():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb WHERE status='waiting'")
    data = cur.fetchall()
    cur.execute("SELECT * FROM regtb WHERE status='Active'")
    data1 = cur.fetchall()
    conn.close()
    return render_template('AdminHome.html', data=data, data1=data1)


@app.route("/ATransactionInfo")
def ATransactionInfo():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transtb")
    data1 = cur.fetchall()
    conn.close()
    return render_template('ATransactionInfo.html', data1=data1)


# ─────────────────────────────────────────────
# User Registration
# ─────────────────────────────────────────────

@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        accno = request.form['accno']
        username = request.form['username']
        Password = request.form['Password']
        bankname = request.form['bankname']
        CPassword = request.form['CPassword']

        if CPassword != Password:
            flash('Password & Retype-Password do not match!')
            return render_template('NewUser.html')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM regtb WHERE username=%s OR AccountNo=%s",
            (username, accno)
        )
        data = cursor.fetchone()

        if data is not None:
            flash('Account Number or Username already registered!')
            conn.close()
            return render_template('NewUser.html')

        cursor.execute(
            "INSERT INTO regtb VALUES ('', %s, %s, %s, %s, %s, %s, %s, %s, 'nill', 'waiting', '0.00', %s)",
            (name, age, mobile, email, address, accno, username, Password, bankname)
        )
        cursor.execute(
            "INSERT INTO multitb VALUES ('', %s, %s)",
            (accno, username)
        )
        conn.commit()

        cur = conn.cursor()
        cur.execute("SELECT * FROM regtb WHERE status='waiting'")
        data = cur.fetchall()
        cur.execute("SELECT * FROM regtb WHERE status='Approved'")
        data1 = cur.fetchall()
        conn.close()
        return render_template('AdminHome.html', data=data, data1=data1)


# ─────────────────────────────────────────────
# User Login
# ─────────────────────────────────────────────

@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['Password']
        session['uname'] = username

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM regtb WHERE username=%s AND Password=%s",
            (username, password)
        )
        data = cursor.fetchone()
        conn.close()

        if data is None:
            flash('Username or Password is wrong')
            return render_template('UserLogin.html')

        session['acc'] = data[6]
        session['pin'] = data[9]
        pin = data[9]

        if pin == "nill":
            return render_template('NewPin.html')
        else:
            return render_template('SelectLogin.html')


# ─────────────────────────────────────────────
# OTP / Forgot Password
# ─────────────────────────────────────────────

@app.route("/getotp", methods=['GET', 'POST'])
def getotp():
    if request.method == 'POST':
        username = request.form['uname']
        session['uname'] = username

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM regtb WHERE username=%s", (username,))
        data = cursor.fetchone()
        conn.close()

        if data is None:
            flash('Username is wrong')
            return render_template('UserLogin.html')

        Phone = data[3]
        Email = data[4]
        n = random.randint(1111, 9999)
        session['ootp'] = n

        sendmsg(Phone, "Your OTP: " + str(n))

        msg = MIMEMultipart()
        fromaddr = "projectmailm@gmail.com"
        msg['From'] = fromaddr
        msg['To'] = Email
        msg['Subject'] = "Alert - Your OTP"
        msg.attach(MIMEText("Your OTP is: " + str(n), 'plain'))

        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(fromaddr, "kkvz xxke jmeb pcyb")
            s.sendmail(fromaddr, Email, msg.as_string())
            s.quit()
        except Exception as e:
            print("Email error:", e)

        return render_template('ForgotPassword.html')


@app.route("/resetpass", methods=['GET', 'POST'])
def resetpass():
    if request.method == 'POST':
        CPassword = request.form['CPassword']
        password = request.form['Password']
        otp = request.form['otp']
        uname = session['uname']

        if int(otp) != int(session['ootp']):
            flash('OTP Incorrect!')
            return render_template('ForgotPassword.html')

        if CPassword != password:
            flash('Password & Retype-Password do not match!')
            return render_template('ForgotPassword.html')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE regtb SET Password=%s WHERE Username=%s",
            (password, uname)
        )
        conn.commit()
        conn.close()
        flash('Password Reset Successfully!')
        return render_template('UserLogin.html')


# ─────────────────────────────────────────────
# PIN Setup & Login
# ─────────────────────────────────────────────

@app.route("/newpin", methods=['GET', 'POST'])
def newpin():
    if request.method == 'POST':
        pin = request.form['pin']
        rpin = request.form['rpin']

        if pin != rpin:
            flash('PIN Mismatch!')
            return render_template('NewPin.html')

        uname = session['uname']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE regtb SET Pin=%s WHERE Username=%s", (pin, uname))
        conn.commit()
        conn.close()
        return render_template('SelectLogin.html')


@app.route("/selectlogin", methods=['GET', 'POST'])
def selectlogin():
    if request.method == 'POST':
        mylist = []

        if request.form["submit"] == "IllusionPin":
            thislist = []
            for x in range(9):
                thislist.append(random.randint(0, 9))
            mylist = list(dict.fromkeys(thislist))
            for x1 in range(10):
                if x1 not in mylist:
                    mylist.append(x1)
            mylist1 = [str(x) + '.png' for x in mylist]
            return render_template('LoginPin.html', data=mylist1, data1=mylist)

        elif request.form["submit"] == "BrightnessPin":
            thislist = []
            for x in range(4):
                thislist.append(random.randint(0, 3))
            mylist = list(dict.fromkeys(thislist))
            for x1 in range(4):
                if x1 not in mylist:
                    mylist.append(x1)
            mylist1 = [str(x) + '.png' for x in mylist]
            session["list"] = mylist1
            return render_template('BrightnessPin.html', data=mylist1)


@app.route("/loginpin", methods=['GET', 'POST'])
def loginpin():
    if request.method == 'POST':
        uname = session['uname']
        pin = request.form.get('seats')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM regtb WHERE pin=%s AND username=%s",
            (pin, uname)
        )
        data = cursor.fetchone()
        conn.close()

        if data is None:
            thislist = [random.randint(0, 9) for _ in range(9)]
            mylist = list(dict.fromkeys(thislist))
            for x1 in range(10):
                if x1 not in mylist:
                    mylist.append(x1)
            mylist1 = [str(x) + '.png' for x in mylist]
            flash("PIN Incorrect!")
            return render_template('LoginPin.html', data=mylist1, data1=mylist)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE temptb")
        conn.commit()
        conn.close()

        import LiveRecognition1 as liv1
        liv1.att()
        del sys.modules["LiveRecognition1"]
        return facelogin()


@app.route("/brightlogin", methods=['GET', 'POST'])
def brightlogin():
    if request.method == 'POST':
        pin0 = request.form['pin0']
        pin1 = request.form['pin1']
        pin2 = request.form['pin2']
        pin3 = request.form['pin3']

        mylist1 = session["list"]
        pos = 0
        for x in mylist1:
            if x == "0.png":
                pos = mylist1.index(x)

        if pos == 0:
            pin0 = 0
        elif pos == 1:
            pin1 = 0
        elif pos == 2:
            pin2 = 0
        elif pos == 3:
            pin3 = 0

        uname = session['uname']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM regtb WHERE username=%s", (uname,))
        data = cursor.fetchone()
        conn.close()

        if data is None:
            return render_template('goback.html', data='Username not found')

        string = data[9]
        string = string[:pos] + '0' + string[pos + 1:]
        string1 = str(pin0) + str(pin1) + str(pin2) + str(pin3)

        if string == string1:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE temptb")
            conn.commit()
            conn.close()

            import LiveRecognition1 as liv1
            del sys.modules["LiveRecognition1"]
            return facelogin()
        else:
            thislist = [random.randint(0, 3) for _ in range(4)]
            mylist = list(dict.fromkeys(thislist))
            for x1 in range(4):
                if x1 not in mylist:
                    mylist.append(x1)
            mylist1 = [str(x) + '.png' for x in mylist]
            session["list"] = mylist1
            flash("Password Incorrect!")
            return render_template('BrightnessPin.html', data=mylist1)


# ─────────────────────────────────────────────
# Face Login & OTP Verify
# ─────────────────────────────────────────────

@app.route("/facelogin")
def facelogin():
    uname = session['uname']
    account = session['acc']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM temptb WHERE AccountNo=%s", (account,))
    data = cursor.fetchone()
    conn.close()

    if data is None:
        flash('Face recognition failed!')
        return render_template('UserLogin.html')

    session['loginuser'] = data[2]
    session['otp'] = data[3]
    return render_template('OTP.html')


@app.route("/verifyotp", methods=['GET', 'POST'])
def verifyotp():
    if request.method == 'POST':
        votp = request.form['votp']
        num = int(session['otp'])
        reversed_num = int(str(num)[::-1])

        if str(reversed_num) == votp:
            uname = session['uname']
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb WHERE username=%s", (uname,))
            data = cur.fetchall()
            conn.close()
            return render_template('UserHome.html', data=data)
        else:
            flash('OTP Incorrect!')
            return render_template('OTP.html')


# ─────────────────────────────────────────────
# User Dashboard
# ─────────────────────────────────────────────

@app.route("/UserHome")
def UserHome():
    uname = session['uname']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb WHERE username=%s", (uname,))
    data = cur.fetchall()
    conn.close()
    return render_template('UserHome.html', data=data)


@app.route("/Transaction")
def Transaction():
    uname = session['uname']
    accno = session['acc']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT AccountNo FROM beneficiarytb WHERE UserName=%s", (uname,))
    data = cur.fetchall()
    conn.close()
    return render_template('Transaction.html', data=data, uname=uname, Accno=accno)


@app.route("/TransactionInfo")
def TransactionInfo():
    uname = session['uname']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM beneficiarytb WHERE UserName=%s", (uname,))
    data = cur.fetchall()
    cur.execute("SELECT * FROM transtb WHERE UserName=%s", (uname,))
    data1 = cur.fetchall()
    conn.close()
    return render_template('TransactionInfo.html', data=data, data1=data1)


# ─────────────────────────────────────────────
# Banking Operations
# ─────────────────────────────────────────────

@app.route("/newbeneficiary", methods=['GET', 'POST'])
def newbeneficiary():
    if request.method == 'POST':
        uname = session['uname']
        aname = request.form['aname']
        accno = request.form['accno']
        Ifsc = request.form['Ifsc']
        bname = request.form['bname']
        address = request.form['address']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO beneficiarytb VALUES ('', %s, %s, %s, %s, %s, %s)",
            (uname, aname, accno, Ifsc, bname, address)
        )
        conn.commit()
        conn.close()
        flash('New Beneficiary Info Saved!')
    return render_template('NewBeneficiary.html')


@app.route("/newmulti", methods=['GET', 'POST'])
def newmulti():
    if request.method == 'POST':
        uname = session['uname']
        Loginuser = session['loginuser']
        jname = request.form['uname']
        accno = session['acc']

        if Loginuser == uname:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO multitb VALUES ('', %s, %s)", (accno, jname))
            conn.commit()
            conn.close()

            import LiveRecognition as liv
            del sys.modules["LiveRecognition"]

            flash('New Join User Info Saved!')
        else:
            flash('You are not the account owner!')
        return render_template('MulitiUser.html')


@app.route("/transaction", methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        uname = session['uname']
        accno = session['acc']
        bacc = request.form['bacc']
        currency = request.form['currency']
        tcc = float(currency)
        date = datetime.datetime.now().strftime('%Y-%b-%d')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM regtb WHERE UserName=%s", (uname,))
        data = cursor.fetchone()
        conn.close()

        if not data:
            return 'User not found!'

        bal = data[11]
        Amount = float(bal) - tcc

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM beneficiarytb WHERE AccountNo=%s", (bacc,))
        bdata = cursor.fetchone()
        conn.close()

        if not bdata:
            return 'Beneficiary not found!'

        bname = bdata[2]

        if Amount < 0:
            flash('Insufficient Balance: ' + str(bal))
            return render_template('Transaction.html')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE regtb SET Balance=%s WHERE UserName=%s", (str(Amount), uname))
        conn.commit()

        num1 = random.randrange(1111, 9999)
        hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))
        cursor.execute("SELECT MAX(id) FROM transtb")
        da = cursor.fetchone()
        hash1 = '0'
        if da and da[0]:
            cursor.execute("SELECT * FROM transtb WHERE id=%s", (da[0],))
            prev = cursor.fetchone()
            if prev:
                hash1 = prev[8]

        cursor.execute(
            "INSERT INTO transtb VALUES ('', %s, %s, %s, %s, %s, %s, %s, %s, 'Transaction')",
            (uname, accno, bname, bacc, currency, date, hash1, hash2)
        )
        conn.commit()
        conn.close()

        flash('Transaction Successful! Balance: ' + str(Amount))
        return render_template('Transaction.html')


@app.route("/amtwithdraw", methods=['GET', 'POST'])
def amtwithdraw():
    if request.method == 'POST':
        uname = session['uname']
        accno = session['acc']
        amt = request.form['amt']
        tcc = float(amt)
        date = datetime.datetime.now().strftime('%Y-%b-%d')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM regtb WHERE UserName=%s", (uname,))
        data = cursor.fetchone()
        conn.close()

        if not data:
            return 'User not found!'

        bal = data[11]
        Amount = float(bal) - tcc

        if Amount < 0:
            flash('Insufficient Balance!')
            return render_template('Withdraw.html')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE regtb SET Balance=%s WHERE UserName=%s", (str(Amount), uname))
        conn.commit()

        num1 = random.randrange(1111, 9999)
        hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))
        cursor.execute("SELECT MAX(id) FROM transtb")
        da = cursor.fetchone()
        hash1 = '0'
        if da and da[0]:
            cursor.execute("SELECT * FROM transtb WHERE id=%s", (da[0],))
            prev = cursor.fetchone()
            if prev:
                hash1 = prev[8]

        cursor.execute(
            "INSERT INTO transtb VALUES ('', %s, %s, %s, %s, %s, %s, %s, %s, 'Withdraw')",
            (uname, accno, uname, accno, amt, date, hash1, hash2)
        )
        conn.commit()
        conn.close()

        flash('Withdrawal Successful! Balance: ' + str(Amount))
        return render_template('Withdraw.html')


@app.route("/deposit", methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        uname = session['uname']
        accno = session['acc']
        amt = request.form['amt']
        date = datetime.datetime.now().strftime('%Y-%b-%d')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM regtb WHERE UserName=%s", (uname,))
        data = cursor.fetchone()
        conn.close()

        if not data:
            return 'User not found!'

        Amount = float(data[11]) + float(amt)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE regtb SET Balance=%s WHERE UserName=%s", (str(Amount), uname))
        conn.commit()

        num1 = random.randrange(1111, 9999)
        hash2 = create_sha256_signature("E49756B4C8FAB4E48222A3E7F3B97CC3", str(num1))
        cursor.execute("SELECT MAX(id) FROM transtb")
        da = cursor.fetchone()
        hash1 = '0'
        if da and da[0]:
            cursor.execute("SELECT * FROM transtb WHERE id=%s", (da[0],))
            prev = cursor.fetchone()
            if prev:
                hash1 = prev[8]

        cursor.execute(
            "INSERT INTO transtb VALUES ('', %s, %s, %s, %s, %s, %s, %s, %s, 'Deposit')",
            (uname, accno, uname, accno, amt, date, hash1, hash2)
        )
        conn.commit()
        conn.close()

        flash('Deposit Successful! Balance: ' + str(Amount))
        return render_template('Deposit.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
