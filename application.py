from flask import Flask
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return "Hello!"

@app.route('/sports')
def find_sports():
    sports = Sport.query.all()

    output = []
    for sport in sports:
        sport_data = {'name': sport.name, "description": sport.description}
    
        output.append(sport_data)
    return {"sports": output}

@app.route('/sports/<id>')
def find_sport(id):
    sport = Sport.query.get_or_404(id)
    return {"name": sport.name, "description": sport.description}

@app.route('/sports', methods=['POST'])
def add_sport():
    sport = Sport(name=request.json['name'], description=request.json['description'])
    db.session.add(sport)
    db.session.commit()
    return {'id': sport.id}

@app.route('/sport/<id>', methods=["DELETE"])
def delete_sport(id):
    sport = Sport.query.get(id)
    if sport is None:
        return{"error": "not found"}
    db.session.delete(sport)
    db.session.commit()
    return {"message": "done!"}

