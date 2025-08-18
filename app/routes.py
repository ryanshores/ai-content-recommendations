from flask import render_template, request, Blueprint
from .forms import IndexForm
from config import client

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = IndexForm(request.form)
    if request.method == 'POST' and form.validate():
        form.output.data = client.get_movie_recommendations(form.input.data)
    return render_template('index.html', form=form)