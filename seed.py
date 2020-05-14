from models import User, Feedback, db
from app import app

db.drop_all()

db.create_all()

user1 = User.register("hokage98", "123", "uzamaki@gmail.com", "naruto", "uzamaki")

db.session.add(user1)
db.session.commit()

feedback1 = Feedback(title="My Feedback", content="lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum", username=user1.username)

db.session.add(feedback1)
db.session.commit()