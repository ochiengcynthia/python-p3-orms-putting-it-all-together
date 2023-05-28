import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id

    @classmethod
    def create_table(cls):
        query = """
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
        )
        """

        CURSOR.execute(query)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()

    def save(self):
        if self.id:
            query = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
            CURSOR.execute(query, (self.name, self.breed, self.id))
            CONN.commit()
        else:
            query = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(query, (self.name, self.breed))
            self.id = CURSOR.lastrowid
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        return cls(row[1], row[2], row[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dogs"
        CURSOR.execute(query)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        query = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(query, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)

    @classmethod
    def find_by_id(cls, dog_id):
        query = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(query, (dog_id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
