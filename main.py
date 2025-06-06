#Импорт
from flask import Flask, render_template,request, redirect, session
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'FJEUOSKCDMVNJF2587485Y6__B458W90JIITK'
#Создание db
db = SQLAlchemy(app)
#Создание таблицы

class Card(db.Model):
    #Создание полей
    #id
    id = db.Column(db.Integer, primary_key=True)
    #Заголовок
    title = db.Column(db.String(100), nullable=False)
    #Описание
    subtitle = db.Column(db.String(300), nullable=False)
    #Текст
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #Вывод объекта и id
    def __repr__(self):
        return f'<Card {self.id}>'    
#Задание №1. Создать таблицу User  
  
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    Cards = db.relationship('Card', backref='author', lazy=True)
    


#Запуск страницы с контентом
@app.route('/', methods=['GET','POST'])
def login():
        error = ""
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            user_db = User.query.all()
            for user in user_db:
                if form_login==user.login:
                    if form_password==user.password:
                        session['user_id']=user.id
                        return redirect('/index')
                    else:
                        error = "Неправильный пароль"
                        return redirect('login.html', error=error)
                else:
                    continue
            
        else:
            return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        
        #Задание №3. Реализовать запись пользователей
        user = User(login=login, password=password)
        
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    
    else:    
        return render_template('registration.html')

#Запуск страницы с контентом
@app.route('/index')
def index():
    #Отображение объектов из БД
    user__id = session.get('user_id')
    card1_id = Card.query.filter_by(user_id=user__id).all()
    return render_template('index.html', cards=card1_id)

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

#Запуск страницы c созданием карты
@app.route('/create')
def create():
    return render_template('create_card.html')

#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']
        user_id = session.get('user_id')
        #Создание объкта для передачи в данных
        card = Card(title=title, subtitle=subtitle, text=text, user_id=user_id)
        db.session.add(card)
        db.session.commit()
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
