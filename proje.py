import random
import time
from datetime import datetime

# داده‌های اولیه
users = {
    "amir@899": {"password": "Q4##56bN", "role": "manager", "fullname": "Amir Ahmadi"},
    "ahmad@sol": {"password": "23Cf@vcvbm", "role": "employee", "fullname": "Ahmad Mosavi", "wallet": 0, "history": [], "email": "", "phone": "", "fav_food": ""},
    "Sia34mak": {"password": "3432SM@12", "role": "employee", "fullname": "Siamak Ansari", "wallet": 0, "history": [], "email": "", "phone": "", "fav_food": ""},
    "Alireza12CV": {"password": "2277020CVVG", "role": "employee", "fullname": "Ali Jamshidi", "wallet": 0, "history": [], "email": "", "phone": "", "fav_food": ""},
    "Amini567": {"password": "20942XsvH@Z", "role": "customer", "fullname": "Ramin Amini", "wallet": 0, "history": [], "email": "", "phone": "", "fav_food": ""},
    "Akbari78887@f": {"password": "35664FTUn45", "role": "customer", "fullname": "Milad Akbari", "wallet": 0, "history": [], "email": "", "phone": "", "fav_food": ""}
}

foods = {
    "Ghormesabzi": 320000,
    "Kabab": 400000,
    "Zereshkpolo": 270000,
    "Berenj": 100000,
    "Ghime": 300000,
    "Khoresht": 220000,
    "Noshabe": 20000,
    "Delester": 35000,
    "Dogh": 20000,
    "Salad": 15000
}

discounts = [
    "QWBv23@#v.3",
    "sd67Hj#!x.2",
    "23FCV%n&5"
]

failed_attempts = {}
lockout_time = {}

# تابع تولید کد تصادفی برای رمز عبور
def generate_random_code():
    return str(random.randint(100000, 999999)) + "FN"

# چک کردن اینکه نام کاربری در فایل موجود باشد یا نه
def check_username_exists(username):
    with open("usernames.txt", "r") as file:
        existing_usernames = file.read().splitlines()
    return username in existing_usernames

# ذخیره نام کاربری جدید در فایل
def save_username_to_file(username):
    with open("usernames.txt", "a") as file:
        file.write(username + "\n")

# تابع ثبت‌نام مشتری
def register_customer():
    while True:
        username = input("نام کاربری جدید: ")
        if len(username) < 5:
            print("خطا: نام کاربری باید حداقل ۵ کاراکتر باشد.")
            continue
        if check_username_exists(username):
            print("خطا: این نام کاربری قبلاً ثبت شده است.")
            continue
        break
# تابع تولید کد تصادفی برای رمز عبور
def generate_random_code():
    random_code = random.randint(100000, 999999)  # تولید یک عدد تصادفی 6 رقمی
    return str(random_code) + "FN"  # اضافه کردن پسوند "FN" به عدد

# تابع ثبت‌نام مشتری
def register_customer():
    username = input("نام کاربری جدید: ")
    while len(username) < 5:
        print("خطا: نام کاربری باید حداقل ۵ کاراکتر باشد.")
        username = input("نام کاربری جدید: ")

    # تولید رمز عبور تصادفی
    random_password = generate_random_code()  # اینجا کد تصادفی ساخته می‌شود
    print(f"رمز عبور تصادفی شما: {random_password}")
    use_random_password = input("آیا می‌خواهید از این رمز عبور استفاده کنید؟ (y/n): ")

    if use_random_password.lower() == "y":
        password = random_password
    else:
        while True:
            password = input("رمز عبور جدید: ")
            if len(password) < 8:
                print("خطا: رمز عبور باید حداقل ۸ کاراکتر باشد.")
                continue
            break  # اگر طول رمز عبور درست باشد، حلقه شکسته می‌شود

    # باقی مراحل ثبت‌نام (مثلاً ذخیره اطلاعات)
    print("ثبت‌نام با موفقیت انجام شد!")

    full_name = input("نام کامل: ")
    email = input("ایمیل: ")
    phone = input("شماره تلفن: ")
    fav_food = input("غذای مورد علاقه: ")

    # ذخیره اطلاعات مشتری در دیکشنری
    users[username] = {
        "password": password,
        "role": "customer",  # نقش کاربر
        "fullname": full_name,
        "email": email,
        "phone": phone,
        "fav_food": fav_food
    }

    # ذخیره نام کاربری جدید در فایل
    save_username_to_file(username)

    print("ثبت‌نام با موفقیت انجام شد!")

# تابع ورود کاربر
def login():
    username = input("نام کاربری: ")
    if username not in failed_attempts:
        failed_attempts[username] = {"count": 0, "lock_time": 0}

    # بررسی اینکه کاربر قفل شده باشد یا خیر
    if failed_attempts[username]["count"] >= 3:
        lock_time = failed_attempts[username]["lock_time"]
        if time.time() - lock_time < 120:  # 2 دقیقه
            print("شما برای مدت ۲ دقیقه قفل شده‌اید. لطفاً دوباره تلاش کنید.")
            return None
        else:
            failed_attempts[username]["count"] = 0  # بازنشانی شمارش تلاش‌ها

    password = input("رمز عبور: ")
    
    # بررسی صحت نام کاربری و رمز عبور
    if username in users and users[username]["password"] == password:
        print(f"ورود موفق! خوش آمدید, {users[username]['fullname']}")
        failed_attempts[username]["count"] = 0  # بازنشانی تلاش‌ها
        return username
    else:
        print("نام کاربری یا رمز عبور اشتباه است.")
        failed_attempts[username]["count"] += 1
        if failed_attempts[username]["count"] >= 3:
            failed_attempts[username]["lock_time"] = time.time()  # ثبت زمان قفل شدن
            print("شما بیش از حد تلاش کرده‌اید. حساب شما برای ۲ دقیقه قفل شد.")
        return None

# اعمال تخفیف
def apply_discount(username, total_price):
    discount_code = input("اگر کد تخفیف دارید وارد کنید: ")
    if discount_code in discounts:
        total_price *= 0.5  # تخفیف 50 درصدی
        print("تخفیف 50 درصدی اعمال شد.")
    
    # بررسی تاریخچه خریدهای قبلی
    total_spent = sum(order["total"] for order in users[username]["history"])
    if total_spent > 250000:
        total_price *= 0.8  # تخفیف 20 درصدی
        print("تخفیف 20 درصدی برای خریدهای قبلی شما اعمال شد.")

    return total_price

# نمایش منوی مشتری
def customer_menu(username):
    cart = []  # سبد خرید مشتری
    while True:
        print("\nمنوی مشتری:")
        print("1. مشاهده لیست غذاها به همراه قیمت آنها")
        print("2. افزودن و حذف غذا از سبد خرید")
        print("3. ثبت نهایی خرید و پرداخت")
        print("4. تغییر اطلاعات مشتری")
        print("5. شارژ کردن کیف پول")
        print("6. مشاهده فاکتورهای خریدهای قبلی")
        print("7. بازگشت به صفحه لاگین")
        
        choice = input("لطفاً یک گزینه وارد کنید: ")

        if choice == "1":
            print("\nلیست غذاها و قیمت‌ها:")
            for food, price in foods.items():
                print(f"{food}: {price} تومان")
        
        elif choice == "2":
            action = input("آیا می‌خواهید غذایی به سبد خرید اضافه کنید یا حذف کنید؟ (add/remove): ").lower()
            if action == "add":
                food_to_add = input("نام غذای مورد نظر برای افزودن به سبد خرید: ")
                if food_to_add in foods:
                    cart.append(food_to_add)
                    print(f"{food_to_add} به سبد خرید اضافه شد.")
                else:
                    print("این غذا در منو موجود نیست.")
            elif action == "remove":
                food_to_remove = input("نام غذای مورد نظر برای حذف از سبد خرید: ")
                if food_to_remove in cart:
                    cart.remove(food_to_remove)
                    print(f"{food_to_remove} از سبد خرید حذف شد.")
                else:
                    print("این غذا در سبد خرید شما موجود نیست.")
            else:
                print("عملیات نامعتبر است.")
        
        elif choice == "3":
            if cart:
                total = sum(foods[food] for food in cart)
                print(f"\nسبد خرید شما: {', '.join(cart)}")
                print(f"قیمت کل: {total} تومان")
            if username in users and "wallet" in users[username]:
                wallet = users[username]["wallet"]
                if wallet >= total:
                  users[username]["wallet"] -= total  # کم کردن هزینه از کیف پول
                  users[username]["history"].append({"items": cart, "total": total})
                  print(f"خرید شما با موفقیت انجام شد. مبلغ {total} تومان از کیف پول شما کسر شد.")
                  cart.clear()  # خالی کردن سبد خرید
                else:
                  print("کیف پول شما کافی نیست.")
            else:
                 print("خطا: اطلاعات کیف پول کاربر موجود نیست.")
        
        elif choice == "4":
            print("\nتغییر اطلاعات مشتری:")
            fullname = input("نام و نام خانوادگی جدید: ")
            email = input("ایمیل جدید: ")
            phone = input("شماره تلفن جدید: ")
            users[username]["fullname"] = fullname
            users[username]["email"] = email
            users[username]["phone"] = phone
            print("اطلاعات شما با موفقیت به روز شد.")
        
        elif choice == "5":
            recharge_amount = int(input("مقدار شارژ کیف پول: "))
            users[username]["wallet"] += recharge_amount
            print(f"کیف پول شما با مبلغ {recharge_amount} تومان شارژ شد.")
        
        elif choice == "6":
            if users[username]["history"]:
                print("\nفاکتورهای خرید قبلی شما:")
                for idx, order in enumerate(users[username]["history"], 1):
                    print(f"\nفاکتور {idx}:")
                    for food in order["items"]:
                        print(f"غذا: {food}, قیمت: {foods[food]} تومان")
                    print(f"قیمت کل: {order['total']} تومان")
            else:
                print("شما هیچ خریدی نداشته‌اید.")
        
        elif choice == "7":
            print("بازگشت به صفحه لاگین.")
            return  # بازگشت به صفحه لاگین
        
        else:
            print("گزینه وارد شده معتبر نیست.")

# اجرای برنامه
while True:
    action = input("لطفاً یکی از گزینه‌های زیر را وارد کنید:\n1. ورود\n2. ثبت‌نام مشتری\n3. بازیابی رمز عبور\n4. خروج\n")
    if action == "1":
        username = login()
        if username:
            customer_menu(username)
        else:
            print("لطفاً دوباره سعی کنید.")
    elif action == "2":
        register_customer()
    elif action == "3":
        recover_password()
    elif action == "4":
        print("خروج از برنامه.")
        break
    else:
        print("گزینه وارد شده معتبر نیست.")

def start():
    while True:
        action = input("لطفاً یکی از گزینه‌های زیر را وارد کنید:\n1. ورود\n2. ثبت‌نام مشتری\n3. بازیابی رمز عبور\n4. خروج\n")
        
        if action == "1":
            username = login()
            if username:
                role = users[username]["role"]
                if role == "manager":
                    manager_menu(username)
                elif role == "employee":
                    employee_menu(username)
                elif role == "customer":
                    customer_menu(username)
            else:
                print("لطفاً دوباره سعی کنید.")
        
        elif action == "2":
            print("ثبت‌نام مشتری...")
        elif action == "3":
            print("بازیابی رمز عبور...")
        elif action == "4":
            print("خروج از برنامه.")
            break
        else:
            print("گزینه وارد شده معتبر نیست.")

start()
# تابع بازیابی رمز عبور
def reset_password():
    username = input("نام کاربری: ")
    if username not in users:
        print("نام کاربری پیدا نشد.")
        return

    email = input("ایمیل خود را وارد کنید: ")
    if email != users[username]["email"]:
        print("ایمیل اشتباه است.")
        return

    phone = input("شماره تلفن خود را وارد کنید: ")
    if phone != users[username]["phone"]:
        print("شماره تلفن اشتباه است.")
        return

    fav_food = input("غذای مورد علاقه شما چیست؟ ")
    if fav_food != users[username]["fav_food"]:
        print("غذای مورد علاقه اشتباه است.")
        return

    # درخواست رمز عبور جدید
    new_password = input("رمز عبور جدید را وارد کنید: ")
    users[username]["password"] = new_password
    print("رمز عبور شما با موفقیت تغییر کرد.")

# منوی اصلی
def main_menu():
    while True:
        print("\nسیستم مدیریت رستوران:")
        print("1. ورود")
        print("2. ثبت‌نام مشتری")
        print("3. بازیابی رمز عبور")
        print("4. خروج")

        choice = input("انتخاب شما: ")

        if choice == "1":
            username = login()
            if username:
                print(f"خوش آمدید, {users[username]['fullname']}")
        elif choice == "2":
            print("ثبت‌نام مشتری")
            register_customer()
        elif choice == "3":
            print("بازیابی رمز عبور")
            reset_password()
        elif choice == "4":
            print("خروج از سیستم.")
            break
        else:
            print("گزینه نامعتبر! لطفاً دوباره تلاش کنید.")

# شروع برنامه
main_menu()

def employee_menu(username):
    while True:
        print("\nلطفاً یکی از گزینه‌های زیر را وارد کنید:")
        print("1. مشاهده لیست غذا ها به همراه قیمت آنها")
        print("2. تغییر لیست موجود غذاها به همراه قیمت آنها")
        print("3. تغییر اطلاعات کارمند")
        print("4. افزودن کدهای تخفیف جدید")
        print("5. مشاهده کلیه فاکتورهای خریدهای قبلی مشتریان")
        print("6. بازگشت به صفحه لاگین")

        action = input("انتخاب شما: ")

        if action == "1":
            # نمایش لیست غذاها به همراه قیمت
            print("\nلیست غذاها و قیمت‌ها:")
            for food, price in foods.items():
                print(f"{food}: {price} تومان")
        
        elif action == "2":
            # تغییر لیست غذاها به همراه قیمت
            food_name = input("نام غذای جدید را وارد کنید: ")
            if food_name in foods:
                new_price = int(input("قیمت جدید این غذا را وارد کنید: "))
                foods[food_name] = new_price
                print(f"قیمت غذای {food_name} با موفقیت تغییر یافت.")
            else:
                print("این غذا در لیست موجود نیست.")

        elif action == "3":
            # تغییر اطلاعات کارمند (نام و نام خانوادگی و نام کاربری غیرقابل تغییر است)
            print("نام و نام خانوادگی و نام کاربری قابل تغییر نیستند.")
            change_field = input("کدام فیلد را می‌خواهید تغییر دهید؟ (ایمیل/شماره تلفن/غذای مورد علاقه): ")
            
            if change_field == "ایمیل":
                new_email = input("ایمیل جدید را وارد کنید: ")
                users[username]["email"] = new_email
                print("ایمیل با موفقیت تغییر یافت.")
            elif change_field == "شماره تلفن":
                new_phone = input("شماره تلفن جدید را وارد کنید: ")
                users[username]["phone"] = new_phone
                print("شماره تلفن با موفقیت تغییر یافت.")
            elif change_field == "غذای مورد علاقه":
                new_fav_food = input("غذای مورد علاقه جدید را وارد کنید: ")
                users[username]["fav_food"] = new_fav_food
                print("غذای مورد علاقه با موفقیت تغییر یافت.")
            else:
                print("فیلد وارد شده معتبر نیست.")

        elif action == "4":
            # افزودن کد تخفیف جدید
            discount_code = input("کد تخفیف جدید را وارد کنید: ")
            discounts.append(discount_code)
            print("کد تخفیف جدید با موفقیت اضافه شد.")

        elif action == "5":
            # مشاهده کلیه فاکتورهای خریدهای قبلی مشتریان
            print("\nفاکتورهای خریدهای قبلی مشتریان:")
            for username, user_data in users.items():
                if user_data["role"] == "customer":
                    print(f"\nکاربر: {user_data['fullname']}")
                    if "history" in user_data:
                        for record in user_data["history"]:
                            items = record["items"]
                            total = record["total"]
                            print(f"غذاها: {', '.join(items)} | مبلغ کل: {total} تومان")
                    else:
                        print("هیچ خریدی ثبت نشده است.")

        elif action == "6":
            # بازگشت به صفحه لاگین
            print("بازگشت به صفحه لاگین.")
            break

        else:
            print("گزینه وارد شده معتبر نیست.")


def manager_menu(username):
    while True:
        print("\nلطفاً یکی از گزینه‌های زیر را وارد کنید:")
        print("1. مشاهده لیست غذا ها به همراه قیمت آنها")
        print("2. تغییر لیست موجود غذاها به همراه قیمت آنها")
        print("3. تغییر اطلاعات کارمندان")
        print("4. تغییر اطلاعات مشتریان")
        print("5. افزودن کدهای تخفیف جدید")
        print("6. مشاهده کلیه فاکتورهای خرید های قبلی")
        print("7. بازگشت به صفحه لاگین")

        action = input("انتخاب شما: ")

        if action == "1":
            # نمایش لیست غذاها به همراه قیمت
            print("\nلیست غذاها و قیمت‌ها:")
            for food, price in foods.items():
                print(f"{food}: {price} تومان")
        
        elif action == "2":
            # تغییر لیست غذاها به همراه قیمت
            food_name = input("نام غذای جدید را وارد کنید: ")
            if food_name in foods:
                new_price = int(input("قیمت جدید این غذا را وارد کنید: "))
                foods[food_name] = new_price
                print(f"قیمت غذای {food_name} با موفقیت تغییر یافت.")
            else:
                print("این غذا در لیست موجود نیست.")
        
        elif action == "3":
            # تغییر اطلاعات کارمندان
            employee_username = input("نام کاربری کارمند را وارد کنید: ")
            if employee_username in users and users[employee_username]["role"] == "employee":
                change_field = input("کدام فیلد را می‌خواهید تغییر دهید؟ (ایمیل/شماره تلفن/غذای مورد علاقه): ")
                
                if change_field == "ایمیل":
                    new_email = input("ایمیل جدید را وارد کنید: ")
                    users[employee_username]["email"] = new_email
                    print("ایمیل کارمند با موفقیت تغییر یافت.")
                elif change_field == "شماره تلفن":
                    new_phone = input("شماره تلفن جدید را وارد کنید: ")
                    users[employee_username]["phone"] = new_phone
                    print("شماره تلفن کارمند با موفقیت تغییر یافت.")
                elif change_field == "غذای مورد علاقه":
                    new_fav_food = input("غذای مورد علاقه جدید را وارد کنید: ")
                    users[employee_username]["fav_food"] = new_fav_food
                    print("غذای مورد علاقه کارمند با موفقیت تغییر یافت.")
                else:
                    print("فیلد وارد شده معتبر نیست.")
            else:
                print("کاربر وارد شده کارمند نیست یا وجود ندارد.")

        elif action == "4":
            # تغییر اطلاعات مشتریان
            customer_username = input("نام کاربری مشتری را وارد کنید: ")
            if customer_username in users and users[customer_username]["role"] == "customer":
                change_field = input("کدام فیلد را می‌خواهید تغییر دهید؟ (ایمیل/شماره تلفن/غذای مورد علاقه): ")

                if change_field == "ایمیل":
                    new_email = input("ایمیل جدید را وارد کنید: ")
                    users[customer_username]["email"] = new_email
                    print("ایمیل مشتری با موفقیت تغییر یافت.")
                elif change_field == "شماره تلفن":
                    new_phone = input("شماره تلفن جدید را وارد کنید: ")
                    users[customer_username]["phone"] = new_phone
                    print("شماره تلفن مشتری با موفقیت تغییر یافت.")
                elif change_field == "غذای مورد علاقه":
                    new_fav_food = input("غذای مورد علاقه جدید را وارد کنید: ")
                    users[customer_username]["fav_food"] = new_fav_food
                    print("غذای مورد علاقه مشتری با موفقیت تغییر یافت.")
                else:
                    print("فیلد وارد شده معتبر نیست.")
            else:
                print("کاربر وارد شده مشتری نیست یا وجود ندارد.")

        elif action == "5":
            # افزودن کد تخفیف جدید
            discount_code = input("کد تخفیف جدید را وارد کنید: ")
            discounts.append(discount_code)
            print("کد تخفیف جدید با موفقیت اضافه شد.")

        elif action == "6":
            # مشاهده کلیه فاکتورهای خرید های قبلی
            print("\nفاکتورهای خریدهای قبلی:")
            for username, user_data in users.items():
                if user_data["role"] in ["customer"]:
                    print(f"\nکاربر: {user_data['fullname']}")
                    if "history" in user_data:
                        for record in user_data["history"]:
                            items = record["items"]
                            total = record["total"]
                            print(f"غذاها: {', '.join(items)} | مبلغ کل: {total} تومان")
                    else:
                        print("هیچ خریدی ثبت نشده است.")

        elif action == "7":
            # بازگشت به صفحه لاگین
            print("بازگشت به صفحه لاگین.")
            break

        else:
            print("گزینه وارد شده معتبر نیست.")

