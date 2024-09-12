# Script to populate tag table with Predetermined tags and Tag Categories
# run in bash with : python populate_tags.py

from models.base import SessionLocal
from models.tag import Tag


def seed_tags():
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
            Tag(name='Good Guy', description='Lover of books', level=1, category='Other')
            # Add more tags as needed
        ]
        print(f"Total number of tags to be added: {len(tags)} {tags}")
        for tag in tags:
            print(
                f"Tag object: id={tag.id}, name={tag.name}, description={tag.description}, level={tag.level}, category={tag.category}")

        # Get names of tags to be added
        tag_names = [tag.name for tag in tags]

        # Check if these tag names already exist in the database
        print("Checking if tags already exist in the database")
        existing_tags = session.query(Tag.name).filter(
            Tag.name.in_(tag_names)).all()
        existing_tag_names = {tag.name for tag in existing_tags}
        print(f"Tags already in the database: {existing_tag_names}")

        # Filter out tags that already exist
        new_tags = [tag for tag in tags if tag.name not in existing_tag_names]
        print(f"Tags that will be added: {[tag.name for tag in new_tags]}")
        print(f"Total number of tags to be added: {len(new_tags)} {new_tags}")
        if new_tags is not None:
            print("Adding new tags to the database")
            session.bulk_save_objects(new_tags)
            session.commit()
            print(f"Inserted {len(new_tags)} new tags.")
        else:
            print("No new tags to insert.")

    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()

    finally:
        print("Closing the database session")
        session.close()


if __name__ == "__main__":
    seed_tags()
