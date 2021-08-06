from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	intro = db.Column(db.String(300), nullable=False)
	intro = db.Column(db.String(300), nullable=False)
	text  = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__ ():
		return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
	return render_template("index.html")


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
	"""
	Router for article creation
	"""
	if request.method == 'POST' and request.form['title'] != ''\
		and request.form['intro'] != '':

		title = request.form['title']
		intro = request.form['intro']
		text = request.form['text']

		article = Article(title=title, intro=intro, text=text)
		try:
			db.session.add(article)
			db.session.commit()
			return redirect('/posts')
		except:
			return "При редактировании статьи произошла ошибка"

	else:
		return render_template("create-article.html")

@app.route('/posts/<int:id>/upd', methods=['POST', 'GET'])
def update_article(id):
	"""
	Router for article updating
	"""
	article = Article.query.get(id)
	if request.method == 'POST' and request.form['title'] != ''\
		and request.form['intro'] != '':

		article.title = request.form['title']
		article.intro = request.form['intro']
		article.text = request.form['text']
		try:
			db.session.commit()
			return redirect('/posts')
		except:
			return "При добавлении статьи произошла ошибка"

	else:	
		return render_template("post_update.html", article=article)


@app.route('/about')
def about():
	"""
	Router for page "about"
	"""
	return render_template("about.html")


@app.route('/posts')
def posts():
	"""
	Router for get all posts
	"""
	articles = Article.query.order_by(Article.date.desc()).all()
	return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
	"""
	Router for get post by id
	"""
	article = Article.query.get(id)
	return render_template("post_detail.html", article=article)

@app.route('/posts/<int:id>/del')
def post_delete(id):
	"""
	Router for deleting post
	"""
	article = Article.query.get_or_404(id)

	try:
		db.session.delete(article)
		db.session.commit()
		return redirect('/posts')
	except:
		return "При удалении статьи произошла ошибка"

if __name__ == '__main__':
	app.run(host = '127.0.0.1', debug=True, port = 1212)