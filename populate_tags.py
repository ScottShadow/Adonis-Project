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
            Tag(name='Gym Shark', description='Your body is your temple!', level=1, category='Exercise and Fitness'),
            Tag(name='Athlete', description='Fitness enthusiast', level=1, category='Exercise and Fitness'),
            Tag(name='Health Freak', description='Passionate about healthy living', level=1, category='Exercise and Fitness'),
            Tag(name='Body Builder', description='Live for the gains', level=1, category='Exercise and Fitness'),
            Tag(name='Sport King', description='Competition is your drug', level=1, category='Exercise and Fitness'),

            Tag(name='Bibliophile', description='Lover of books', level=1, category='Learning and Education'),
            Tag(name='Scholar', description='Chasing that knowledge!', level=1, category='Learning and Education'),
            Tag(name='Programmer', description='Lover of books', level=1, category='Learning and Education'),
            Tag(name='Scholar', description='Lover of books', level=1, category='Learning and Education'),
            Tag(name='Scholar', description='Lover of books', level=1, category='Learning and Education'),
            Tag(name='Scholar', description='Lover of books', level=1, category='Learning and Education'),

            Tag(name='Social Butterfly', description='People are your power!', level=1, category='Social Interaction'),
            Tag(name='Life of the Party', description='Never a dull time around you!', level=1, category='Social Interaction'),
            Tag(name='Mediator', description='You bring people together!', level=1, category='Social Interaction'),
            Tag(name='Introvert', description='Time alone is time well spent!', level=1, category='Social Interaction'),
            Tag(name='Night Owl', description='You live for the nightlife!', level=1, category='Social Interaction'),

            Tag(name='Code Junkie', description='Eat.Sleep.Code.Repeat.', level=1, category='Other'),
            Tag(name='Teacher', description='Lover of books', level=1, category=''),
            Tag(name='Lover', description='Lover of books', level=1, category='Other'),
            Tag(name='Friend', description='Lover of books', level=1, category='Other'),
            Tag(name='Good Guy', description='Lover of books', level=1, category='Other'),

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
