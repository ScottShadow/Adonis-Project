# Script to populate tag table with Predetermined tags and Tag Categories
# run in bash with : python populate_tags.py

from models.base import SessionLocal
from models.tag import Tag

def seed_tags():
    # Initialize database session
    session = SessionLocal()
     try:
        # Define tags to be added
        tags = [
            Tag(id='1', name='gym shark', description='Fitness enthusiast', level=1, category='self improvement'),
            Tag(id='2', name='bibliophile', description='Lover of books', level=1, category='self improvement'),
            # Add more tags as needed
        ]

        # Check for existing tags to avoid duplicates
        existing_tags = {tag.name for tag in session.query(Tag).all()}
        new_tags = [tag for tag in tags if tag.name not in existing_tags]

        if new_tags:
            session.bulk_save_objects(new_tags)
            session.commit()
            print(f"Inserted {len(new_tags)} new tags.")
        else:
            print("No new tags to insert.")

    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    seed_tags()
