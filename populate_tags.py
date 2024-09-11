# Script to populate tag table with Predetermined tags and Tag Categories
# run in bash with : python populate_tags.py

from models.base import SessionLocal
from models.tag import Tag


def seed_tags():
    session = SessionLocal()
    print("Starting to seed tags")

    try:
        tag_1 = Tag(id='1', name='gym shark', description='Fitness enthusiast',
                    level=1, category='self improvement')
        print(
            f"Tag object: id={tag_1.id}, name={tag_1.name}, description={tag_1.description}, level={tag_1.level}, category={tag_1.category}")
        # Define tags to be added
        tags = [
            Tag(name='gym shark', description='Fitness enthusiast',
                level=1, category='self improvement'),
            Tag(name='bibliophile', description='Lover of books',
                level=1, category='self improvement'),
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
