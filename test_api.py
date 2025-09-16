import os
import sys
import unittest
import json
import datetime
from flask import Flask
from flask_testing import TestCase

# Aggiungi la directory principale al path per importare i moduli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.user import db, User
from src.models.trail import Trail
from src.models.equipment import Equipment
from src.models.refuge import Refuge
from src.models.trip_log import TripLog
from src.models.guide import Guide, UserGuideProgress

# Crea una versione semplificata dell'app per i test
def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    return app

class MountainHubAPITest(unittest.TestCase):
    """Test case per le API di MountainHub"""
    
    def setUp(self):
        """Setup per ogni test"""
        self.app = create_test_app()
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self._create_test_data()
    
    def tearDown(self):
        """Cleanup dopo ogni test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _create_test_data(self):
        """Crea dati di test nel database"""
        with self.app.app_context():
            # Crea utente di test
            test_user = User(
                username='test_user',
                email='test@example.com',
                password_hash='hashed_password'
            )
            db.session.add(test_user)
            db.session.commit()
            
            # Crea trail di test
            test_trail = Trail(
                name='Monte Test',
                description='Un sentiero di test',
                difficulty='moderate',
                length_km=10.5,
                elevation_gain=800,
                estimated_time_hours=4.5,
                start_point='Punto di partenza',
                end_point='Punto di arrivo',
                region='Valle Test',
                country='Italia',
                coordinates={'start': {'lat': 45.9, 'lng': 7.6}, 'end': {'lat': 46.0, 'lng': 7.7}}
            )
            db.session.add(test_trail)
            db.session.commit()
            
            # Crea equipment di test
            test_equipment = Equipment(
                name='Scarponi da trekking',
                brand='TestBrand',
                model='TestModel',
                category='footwear',
                subcategory='hiking_boots',
                description='Scarponi da trekking di test',
                price_range={'min': 100, 'max': 150},
                weight=850,
                rating=4.5,
                skill_level_required='beginner',
                season_use=['spring', 'summer', 'autumn']
            )
            db.session.add(test_equipment)
            db.session.commit()
    
    # Test di base per verificare che il setup funzioni
    def test_setup(self):
        """Test per verificare che il setup funzioni correttamente"""
        with self.app.app_context():
            users = User.query.all()
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0].username, 'test_user')
            
            trails = Trail.query.all()
            self.assertEqual(len(trails), 1)
            self.assertEqual(trails[0].name, 'Monte Test')
            
            equipment = Equipment.query.all()
            self.assertEqual(len(equipment), 1)
            self.assertEqual(equipment[0].name, 'Scarponi da trekking')

if __name__ == '__main__':
    unittest.main()

