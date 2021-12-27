from flask import Flask, request,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__) # instance app

app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Test=12345@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATION = False
)
db =SQLAlchemy(app)

#BASIC ROUTE
@app.route('/index')
@app.route('/')
def hello_flask():
    return 'Hello flask'

@app.route('/new/')
#def query_strings():  #user enter /new/?greeting= hola!
def query_strings(greeting = 'hello'):  # user not  enter
    #query_val = request.args.get('greeting')
    query_val = request.args.get('greeting', greeting)  #go check localhost:5000/new/
    return '<h1> the greeting is : {0} </h1>'.format(query_val)

@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='mina'):
    return '<h1> hello there !  {} ' '</h1>'.format(name)
 #go check localhost:5000/user   hello there ! mina
#go check localhost:5000/user/jonathan   hello there ! jonathan

#go check localhost:5000/user/17   hello there ! 17

#STRINGS
@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> here is a string: ' + name + '</h1>'
#localhost:5000/text/hello there
#NUMBERS
@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1> the number you picked is: ' + str(num) + '</h1>'
#check localhost:5000/numbers/58 #type error: can't convert 'int' object to str implicitly  add str(num) the number you picked is: 58
# localhost:5000/numbers/58.25  Not Found
#NUMBER
@app.route('/add/<int:num1>/<int:num2>')
def adding_intergers(num1,num2):
    return '<h1> the sum is: {}'.format(num1+num2)  + '</h1>'
#FLOAT
@app.route('/product/<float:num1>/<float:num2>')
def product_two_numbers(num1,num2):
    return '<h1> the product is: {}'.format(num1*num2)  + '</h1>'
#localhost:5000/product/25.20/86.0  the sum is: 111

#USING TEMPLATE  this folder was created manually and also hello.html since free version not support Flask template
from flask import render_template
@app.route('/temp')
def using_template():
    return render_template('hello.html')
#localhost:5000/temp Hello,Welcome Home...
#This is from the html file

#JINJA TEMPLATES

@app.route('/watch')
def top_movies():
    movie_list= ['autopsy of jane doe', 'neon demon', 'ghost in a shell', 'kong: skull island', 'john wick 2', 'spiderman - homecoming']
    return render_template('movies.html', movies=movie_list, name='Harry')
#localhost:5000/watch Movies to watch  This collection belongs toHarry
# to pass movie_list, code h3 in movies.html
#localhost:5000/watch
"""Movies to watch
This collection belongs toHarry
movies: ['autopsy of jane doe', 'neon demon', 'ghost in a shell', 'kong: skull island', 'john wick 2', 'spiderman - homecoming']
first: autopsy of jane doe
slicing: ['neon demon', 'ghost in a shell', 'kong: skull island']"""
# better way to write something html tag movies.html

#add for ul and li in movies.html
#localhost:5000/watch


@app.route('/table')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 02.14,
                  'neon demon': 3.20,
                  'ghost in a shell': 1.50,
                  'kong: skull island': 3.50,
                  'john wick 2': 02.52,
                  'spiderman - homecoming': 1.40}
    return render_template('table_data.html', movies=movies_dict, name='Sally')
#localhost:5000/table  # name in @app


# localhost:5000/table


#built styles.css in static/css and link to table_data.html and run again
#localhost:5000/table  there is  path to the file


@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.40}
    return render_template('filter_data.html', movies=movies_dict, name=None, film='a christmas carol')
#localhost:5000/filters

@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.40}
    return render_template('using_macros.html', movies=movies_dict)
#localhost:5000/macros
class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    def __init__(self,  name):  #for 23 remove id

        self.name = name
    def __repr__(self):
        #return 'The id is {}, Name is {}'.format(self.id, self.name)
        return 'Publisher is {}'.format(self.name)  # make it automatic

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())
    #relationship
    pub_id = db.column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self,  title, author, avg_rating, book_format, image, num_pages, pub_id):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format  # (psycopg2.ProgrammingError) can't adapt type 'builtin_function_or_method' book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return ' {} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)