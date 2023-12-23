import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from forms import add_coffee_form

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)
db = SQLAlchemy()
if os.environ.get('LOCAL') == "True":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
db.init_app(app)


class cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    map_url = db.Column(db.String(1000), nullable=False, unique=True)
    img_url = db.Column(db.String(1000), nullable=False)
    location = db.Column(db.String(1000), nullable=False)
    has_sockets = db.Column(db.Integer, default=0, nullable=False)
    has_toilet = db.Column(db.Integer, default=0, nullable=False)
    has_wifi = db.Column(db.Integer, default=0, nullable=False)
    can_take_calls = db.Column(db.Integer, default=0, nullable=False)
    seats = db.Column(db.String(200), nullable=False)
    coffee_price = db.Column(db.Float, nullable=False)


with app.app_context():
    # db.create_all()


    @app.route('/')
    def index():
        names = db.session.execute(db.select(cafe).order_by(cafe.name)).scalars()
        return render_template("index.html", names=names)


    @app.route('/Add_Cafe', methods=["GET", "POST"])
    def add_coffe():
        form = add_coffee_form()
        if form.validate_on_submit():
            new_cafe = cafe(name=form.name.data, map_url=form.map_url.data, img_url=form.img_url.data,
                            location=form.location.data, has_sockets=form.has_sockets.data,
                            has_toilet=form.has_toilet.data, has_wifi=form.has_wifi.data,
                            can_take_calls=form.can_take_calls.data, seats=form.seats.data,
                            coffee_price=form.coffee_price.data)
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('add.html', form=form)


    @app.route('/Show_Cafe/<int:cafe_id>', methods=["GET", "POST"])
    def show_cafe(cafe_id):
        socket = 'No'
        toilet = 'No'
        wifi = 'No'
        calls = 'No'
        requested_cafe = db.get_or_404(cafe, cafe_id)
        if requested_cafe.has_sockets:
            socket = 'Yes'
        if requested_cafe.has_toilet:
            toilet = 'Yes'
        if requested_cafe.has_wifi:
            wifi = 'Yes'
        if requested_cafe.can_take_calls:
            calls = 'Yes'
        return render_template('cafe.html', cafe=requested_cafe, socket=socket, toilet=toilet, wifi=wifi, calls=calls)


    @app.route('/Edit_Cafe/<int:cafe_id>', methods=["GET", "POST"])
    def edit_coffe(cafe_id):
        cafe_to_edit = db.get_or_404(cafe, cafe_id)
        edit_form = add_coffee_form(name=cafe_to_edit.name, map_url=cafe_to_edit.map_url, img_url=cafe_to_edit.img_url,
                                    location=cafe_to_edit.location, has_sockets=cafe_to_edit.has_sockets,
                                    has_toilet=cafe_to_edit.has_toilet,
                                    has_wifi=cafe_to_edit.has_wifi, can_take_calls=cafe_to_edit.can_take_calls,
                                    seats=cafe_to_edit.seats, coffee_price=cafe_to_edit.coffee_price)
        if edit_form.validate_on_submit():
            cafe_to_edit.name = edit_form.name.data
            cafe_to_edit.map_url = edit_form.map_url.data
            cafe_to_edit.img_url = edit_form.img_url.data
            cafe_to_edit.location = edit_form.location.data
            cafe_to_edit.has_sockets = edit_form.has_sockets.data
            cafe_to_edit.has_wifi = edit_form.has_wifi.data
            cafe_to_edit.can_take_calls = edit_form.can_take_calls.data
            cafe_to_edit.seats = edit_form.seats.data
            cafe_to_edit.coffee_price = edit_form.coffee_price.data
            return redirect(url_for('index'))
        return render_template('edit.html', form=edit_form, is_edit=True)


    @app.route("/delete/<int:cafe_id>")
    def delete_cafe(cafe_id):
        cafe_to_delete = db.get_or_404(cafe, cafe_id)
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return redirect(url_for('index'))


    if __name__ == "__main__":
        app.run(debug=True, port=5000)
