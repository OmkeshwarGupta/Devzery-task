from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testcases_su3p_user:5msdLRLPJiBCqOPap2hDGKz3GOO7bvNi@dpg-cqg8rhaju9rs73c9g6rg-a.oregon-postgres.render.com/testcases_su3p'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    estimate_time = db.Column(db.Integer)
    module = db.Column(db.String(100))
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create the table and add sample data
def create_and_seed_db():
    with app.app_context():
        db.create_all()
        # Check if there are existing records
        if TestCase.query.count() == 0:
            # Add sample data
            sample_data = [
                TestCase(name='Test Case 1', estimate_time=5, module='Onboarding', priority='Low', status='Select'),
                TestCase(name='Test Case 2', estimate_time=5, module='User Log In', priority='Medium', status='Select'),
                TestCase(name='Test Case 3', estimate_time=5, module='Password', priority='High', status='Select'),
            ]
            db.session.bulk_save_objects(sample_data)
            db.session.commit()

create_and_seed_db()

@app.route('/testcases', methods=['GET'])
def get_testcases():
    testcases = TestCase.query.order_by(TestCase.id).all()
    return jsonify([{
        'id': tc.id,
        'name': tc.name,
        'estimate_time': tc.estimate_time,
        'module': tc.module,
        'priority': tc.priority,
        'status': tc.status,
        'last_updated': tc.last_updated
    } for tc in testcases])

@app.route('/testcases/<int:id>', methods=['PUT'])
def update_status(id):
    data = request.get_json()
    test_case = TestCase.query.get(id)
    if not test_case:
        return jsonify({'message': 'Test case not found'}), 404

    test_case.status = data['status']
    
    db.session.commit()
    return jsonify({'message': 'Status updated'})

if __name__ == '__main__':
    app.run(debug=True)
