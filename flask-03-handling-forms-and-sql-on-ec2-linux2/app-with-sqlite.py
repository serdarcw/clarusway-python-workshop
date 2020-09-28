# Import Flask modules
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy # sql ile ilgili işlem yapacağımız için flask altında çalışan sqlalchemy library'sini yüklememiz gerekiyor. Bu library herhangi bir database e python ile ulaşmak için yeterli olacaktır. sql alchemy'nin pip kullanılarak yüklü olması gerekit. Bunun için şu komut kullanılır; pip list ---> SQL alchemy olduğu görülür. Eğer yoksa şu komut çalıştırılarak flask üzerinde sql alchemy install edilir; "pip install flask_sqlalchemy"... Eğer sizde varsa halihazırda yüklü mesajı çıkacaktır.

# Create an object named app
app = Flask(__name__) #Burada bir application create ettiğimizi söyluyoruz

# Configure sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./email.db' # Peki ben ORM ile kendi oluşturduğum veritabanını nasıl birleştireceğim. işte o  da burasında yapılıyor. Biz burada "SQLALCHEMY_DATABASE_URI" kısmına bizim database'imizin nerde olduğunu verirsek o zaman ORM ile bizim veritabanımızın bağlantısını kurmuş oluyoruz. Burada bir configuration ismi veriyorum. config, app aplication içinde bir dictionary. Bu şunu söylüyor, bu database sql database demiş oluyor. . ---> current dir ve orada  database'in ismini veriyorum. Burada email.db benim database ismim oluyor. Burada databaseyoksa bu komut orada bir bu isimde bir database oluşturur. 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False # Bu parametreye de ihtiyacımız var. Default olarak None atanır ve sql alchemy'deki tüm modifikasyonları takip eder ve sinyal olarak yayınmasını sağlar. Fakat bu sistemde bir overload oluşturur yani ekstra memory gerektirir. Development env de olsaydık iyi bir özellik ama şu an için buna ihtiyaç yok. Ondan bunu yazıyoruz. 

db = SQLAlchemy(app) # bir db oluşturuyorum sql alchemy bu app içerisinde bu özellikler çerçevesinde bir database oluşturulmasını sağlayacaktır. Bu şekilde aslında python tarafı ile sql achemy i birleştirmiş oluyoruz





# Execute the code below only once.
# Write sql code for initializing users table..

drop_table = 'DROP TABLE IF EXISTS users;'   # Burada 3 variable tanımlıyorum. Bunlar sql statements lardır. Bu birincisi eğer böyle bir tablo varsa onu indirmeye yöneliktir.
users_table = """    
CREATE TABLE users(
username VARCHAR NOT NULL PRIMARY KEY,
email VARCHAR);
""" # email.db içerisinde users table oluşturmak için yazılmıştır bu query
data = """
INSERT INTO users
VALUES
	("Buddy Rich", "buddy@clarusway.com" ),
	("Candido", "candido@clarusway.com"),
	("Charlie Byrd", "charlie.byrd@clarusway.com");
"""   # Bu query de database içerisine 3 tane kayıt atmaya yarar.

db.session.execute(drop_table)  # Bunları run etmemiz lazım. elimde db database'i var. run etmek için şu komutlar kullanılır
db.session.execute(users_table)
db.session.execute(data)
db.session.commit()  # Bu statementları çalıştırdıktan sonra bunları commit etmek lazım. Bunu, çalıştırılan bu komutları perminent yapmak için kullanıyorum. Bu 4 fonksiyon sadece execution içindir.  Ne zaman ben bu app i çalıştırsam başlangıçta bu querry ler run edilecektir. Dolayısı ile bu komutlar başta bir kere çalıştırılır. İkinci defa bu komutları buradan çıkaracağım yoksa elimdeki girilen dataları kaybederim. Bunu göreceğiz. 






# Write a function named `find_emails` which find emails using keyword from the user table in the db,
# and returns result as tuples `(name, email)`. -----> application'ımız dynamic bir app. Bize verilen keyword kullanılarak user table içerisinde keyword varsa bulacak ve bize response geri dönecek. Bulamazsa da ona göre bir response dönmesini istiyorum.
def find_emails(keyword):   # ---> keyword argument 
    query=f"""
    SELECT * FROM users WHERE username LIKE '%{keyword}%';
    """
    result = db.session.execute(query)  # Bu query i çalıştırıp çıkan değeri result variable olarak atıyorum. Bu bir list olarak geri döner. result bana row'lar olarak geri dönecektir. Benim bunu user email halinde döndürmem lazım
    user_emails = [(row[0], row[1]) for row in result]
    if not any(user_emails):
        user_emails=[('Not Found', 'Not Found')]   # Eğer herhangi bir kayıt bulunmaz ise bu durumda karşımıza çıkacak mesajı burada yazıyoruz. Bu durumda dummy create ediyorum ve bu da tuple tipinde olacaktır. Bu sonuç, herhangi bir result olmaması durumunda işe yarayacak
    return user_emails





# Write a function named `insert_email` which adds new email to users table the db.
def insert_email(name, email):    # ekleme yapmak istediğimizde bizim iki argument'a ihtiyacımız var 
    query=f"""
    SELECT * FROM users WHERE username LIKE '{name}';
    """
    result = db.session.execute(query)
    #default response
    response = 'Error occured...'
    # if user input are None (null) give warning
    if name == "" or email == "":
        response = 'Username or email can not be empty!!'
    # if there is no same user name in the db, then insert the new one
    elif not any(result):
        insert =f"""
        INSERT INTO users
        VALUES ('{name}', '{email}')
        """
        result = db.session.execute(insert)  
        db.session.commit()                         # biz yeni bir değişken koyduğumzda bunu commit etmek zorundayız
        response= f'User {name} added successfully'
    # if there is user with same name, then give warning
    else:
        response = f'User {name} already exits.'
    
    return response

# Yukarıdaki bu iki fonksiyon database ile ilişkiye girecek olabn kısmı oluşturuyor



# Write a function named `emails` which finds email addresses by keyword using `GET` and `POST` methods,
# using template files named `emails.html` given under `templates` folder
# and assign to the static route of ('/')
@app.route('/', methods = ['GET', 'POST'])
def emails():
    if request.method == 'POST':
        user_name = request.form['username']
        user_emails = find_emails(user_name)
        return render_template('emails.html', name_emails=user_emails, keyword=user_name, show_result=True)
    else:
        return render_template('emails.html', show_result=False)


# Write a function named `add_email` which inserts new email to the database using `GET` and `POST` methods,
# using template files named `add-email.html` given under `templates` folder
# and assign to the static route of ('add')
@app.route('/add', methods=['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        user_name = request.form['username']
        user_email = request.form['useremail']
        result = insert_email(user_name, user_email)
        return render_template('add-email.html', result=result, show_result=True)
    else:
        return render_template('add-email.html', show_result=False)


# Add a statement to run the Flask application which can be reached from any host on port 80.
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=80)