from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from stories import Story, stories

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)

@app.route('/home')
def show_home():
    """shows homepage: allows user to select story"""

    story_ids = stories.keys()

    return render_template('home.html', stories=story_ids)

@app.route('/madlib-form')
def show_form():
    """shows form page: allows user to fill in prompts for selected story"""

    story_id = int(request.args.get('story-choice'))
    story = stories[story_id]
    prompts = story.prompts
    
    return render_template('form.html', prompts=prompts, story=story_id)

@app.route('/story/<int:storyid>')
def show_story(storyid):
    """shows story page: generates story text based on stroy template and user answers"""

    story = stories[storyid]
    answers = dict()
    for prompt in story.prompts:
        answers[prompt] = request.args.get(prompt)
    text = story.generate(answers)

    return render_template('story.html', text=text)

