from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uniquecoding123:ZHwPNI5tja8G@ep-fragrant-dust-96359711.ap-southeast-1.aws.neon.tech/winner?sslmode=require'
#postgresql://teja:i7ycxkpol_MY14dpeMRV-A@silky-insect-7435.8nk.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create a Team model
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    @property
    def total_marks(self):
        return self.wins + self.draws + self.losses


# Create tables in the database
app.app_context().push()

@app.route('/')
def index():
    teams = Team.query.all()
    return render_template('index.html', teams=teams)

@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        team_name = request.form['team_name']
        wins = int(request.form['wins'])
        draws = int(request.form['draws'])
        losses = int(request.form['losses'])

        # Check if the team already exists
        existing_team = Team.query.filter_by(name=team_name).first()

        if existing_team:
            # Update the existing team
            existing_team.wins += wins
            existing_team.draws += draws
            existing_team.losses += losses
        else:
            # Create a new team
            new_team = Team(name=team_name, wins=wins, draws=draws, losses=losses)
            db.session.add(new_team)

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_team.html')


@app.route('/clear_db')
def clear_db():
    # Clear all records from the Team table
    Team.query.delete()

    # Commit the changes
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

