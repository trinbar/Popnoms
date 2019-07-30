from model import User, Bookmark, db, connect_to_db
from datetime import datetime

def example_data():
    """Sample data for tests file."""

    #Fake users
    user1 = User(user_id=1, 
        name = 'Trinity Dunbar',
        username = 'trinbar',
        password = 'password',
        email='dunbar.trinity@gmail.com',
        location = 'San Francisco, CA, USA',
        )

    user2 = User(user_id=2, 
        name ='Trinity Gaerlan',
        username = 'trigaer',
        password = 'password',
        email = 'tmgaerlan@gmail.com',
        loation = 'Oakland, CA, USA',)

    #Fake bookmarks
    bookmark1 = Bookmark(bookmark_id=1, 
        bookmark_type = 1,
        event_id ='62010309505',
        user_id = 1,
        timestamp = datetime.now())

    bookmark2 = Bookmark(bookmark_id = 2, 
        bookmark_type_id = 2,
        event_id='62010309505',
        user_id = 2,
        timestamp = datetime.now())
    

db.session.add_all([user1, user2, bookmark1, bookmark2])
db.session.commit()