# Script to populate tag table with Predetermined tags and Tag Categories
# run in bash with : python populate_tags.py

from api.v1.app import app, db
from models.tag import Tag

def seed_tags():
    with app.app_context():
        # Define tags to be added
        tags = [
            Tag(id='1', name='gym shark', description='Fitness enthusiast', level=1, category='self improvement'),
            Tag(id='2', name='bibliophile', description='Lover of books', level=1, category='self improvement'),
            # Add more tags as needed, more will be added ♥
        ]
        
        # Check for existing tags to avoid duplicates
        existing_tags = {tag.name for tag in Tag.query.all()}
        new_tags = [tag for tag in tags if tag.name not in existing_tags]
        
        if new_tags:
            db.session.bulk_save_objects(new_tags)
            db.session.commit()
            print(f"Inserted {len(new_tags)} new tags.")
        else:
            print("No new tags to insert.")

if __name__ == "__main__":
    seed_tags()