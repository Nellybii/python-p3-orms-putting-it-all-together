import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs;
        """
        CURSOR.execute(sql)

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))

            self.id = CURSOR.lastrowid

            CONN.commit()
        else:
            sql = """
                UPDATE dogs
                SET name = ?, breed = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs;
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None

    @classmethod
    def find_by_id(cls, dog_id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        CURSOR.execute(sql, (dog_id,))
        row = CURSOR.fetchone()
        if row:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name_and_breed(name, breed)
        if existing_dog:
            return existing_dog
        else:
            new_dog = cls.create(name, breed)
            return new_dog

    @classmethod
    def find_by_name_and_breed(cls, name, breed):
        sql = """
            SELECT * FROM dogs
            WHERE name = ? AND breed = ?;
        """
        CURSOR.execute(sql, (name, breed))
        row = CURSOR.fetchone()
        if row:
            dog = cls.new_from_db(row)
            return dog
        else:
            return None

    def update(self, new_name):
        if self.id is not None:
            sql = """
                UPDATE dogs
                SET name = ?
                WHERE id = ?;
            """
            CURSOR.execute(sql, (new_name, self.id))
            CONN.commit()
            self.name = new_name
        else:
            raise ValueError("Cannot update name before saving to the database")
