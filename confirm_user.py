from albumy import db
from albumy.models import User
user = User.query.filter_by(username='testuser').first()
if user:
    user.confirmed = True
    db.session.commit()
    print('User confirmed\!')
else:
    print('User not found\!')
