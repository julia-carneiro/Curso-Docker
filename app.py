# app.py
from flask import Flask, request, render_template, redirect, url_for
import pymongo
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
mongo_uri = "mongodb+srv://root:pass@cursocrawler.vybbjvd.mongodb.net/tasks"

def get_db():
    client = MongoClient(mongo_uri)
    db = client['db_tasks']
    return db

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Rota para a página inicial
@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        data = request.form
        title = data.get('title')
        description = data.get('description')

        if title and description:
            db = get_db()
            task = {
                'title': title,
                'description': description,
                'done': False
            }
            db.tasks.insert_one(task)

    db = get_db()
    tasks = list(db.tasks.find({}, {'_id': True, 'title': True, 'description': True}))
    return render_template('index.html', tasks=tasks)



@app.route('/delete/<string:task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    db = get_db()
    print(f"ID da tarefa a ser excluída: {task_id}")

    result = db.tasks.delete_one({'_id': ObjectId(task_id)})
    if result.deleted_count > 0:
        print(f"Tarefa com ID {task_id} excluída com sucesso.")
    else:
        print(f"Tarefa com ID {task_id} não encontrada.")

    return redirect('/')



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
