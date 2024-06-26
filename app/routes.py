from flask import render_template, flash
from app import app
from app.forms import AddQueryForm, EditQueryForm, EditSettingsForm, ChatForm
from app.ai  import Createsummary, askchat
from app.models import Prompts, SummarySettings, ChatAnswer
from app import db
import json

@app.route("/hello")
def hello_world():

    return render_template('base.html')



@app.route('/edit', methods=['GET', 'POST'])
def edit():

    print("YES")
    all_prompts=Prompts.query.all()

    form = EditQueryForm()
    
    return render_template('edit.html', form=form, all_prompts=all_prompts)



@app.route('/edit/<id>', methods=['GET', 'POST'])
def editprompt(id):

    print("this is the ID"+ id)
    prompt = Prompts.query.filter_by(id=id).first_or_404()
    form = EditQueryForm()

    
    print(prompt)

    if form.validate_on_submit():
        prompt.content = form.querycontent.data
        prompt.gsheetcell = form.cell.data
        db.session.commit()
        flash('Your changes have been saved.')

    return render_template('editprompt.html', form=form, prompt=prompt)

@app.route('/', methods=['GET', 'POST'])
def createsummary():
    settings= SummarySettings.query.filter_by(id=1).first_or_404()
    return render_template('createsummary.html', settings=settings)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    form = ChatForm()
    settings= SummarySettings.query.filter_by(id=1).first_or_404()
    res= ChatAnswer
    if form.validate_on_submit():
        query = form.query.data
        print(query)
        answer = askchat(settings, query)
        print(answer)
        res.content = answer.content
        
    return render_template('chat.html', settings=settings, form = form, res = res)




@app.route('/created', methods=['GET', 'POST'])
def created():
    query_set= Prompts.query.all()
    settings= SummarySettings.query.filter_by(id=1).first_or_404()

    print(settings)
    print(query_set)
    Createsummary(settings, query_set)
    print("Summary created successful")
    return render_template('created.html')


@app.route('/editsettings', methods=['GET', 'POST'])
def updatesettings():
    settings= SummarySettings.query.filter_by(id=1).first_or_404()
    form = EditSettingsForm()

    if form.validate_on_submit():
        settings.companyname = form.companyname.data
        settings.gsheetname = form.gsheetname.data
        settings.gsheetno = form.gsheetno.data
        settings.indexname = form.indexname.data
        settings.llm = form.llm.data
        settings.embedding = form.embedding.data
        settings.rag_prompt = form.RAG_Prompt.data

        db.session.commit()

    return render_template('updatesettings.html', settings=settings, form = form)