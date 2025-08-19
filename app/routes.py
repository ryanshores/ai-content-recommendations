from flask import render_template, request, Blueprint, Response
from .forms import IndexForm
from .client import get_mood_recommendation, get_mood_recommendation_stream

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = IndexForm(request.form)
    if request.method == 'POST' and form.validate():
        form.output.data = get_mood_recommendation(form.input.data)
    return render_template('index.html', form=form)

@main.route('/stream', methods=['GET'])
def stream():
    input = request.args.get('input')

    if input:
        return Response(get_mood_recommendation_stream(input), mimetype='text/event-stream')

    return render_template('stream.html', form=IndexForm())

