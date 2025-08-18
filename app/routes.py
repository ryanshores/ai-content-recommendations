from flask import render_template, request, Blueprint
from .forms import IndexForm
from .client import get_mood_recommendation

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = IndexForm(request.form)
    if request.method == 'POST' and form.validate():
        form.output.data = get_mood_recommendation(form.input.data)
    return render_template('index.html', form=form)