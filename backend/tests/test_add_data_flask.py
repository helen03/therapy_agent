from backend import db, create_app
from backend.models import User

app = create_app()

u = User(username='john', email='john@example.com')
db.session.add(u)
db.session.commit()
