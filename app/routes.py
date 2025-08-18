from flask import render_template, request, Blueprint
from .client import get_data
from .forms import IndexForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = IndexForm(request.form)
    if request.method == 'POST' and form.validate():
        form.output.data = get_data(form.input.data)
    return render_template('index.html', form=form)