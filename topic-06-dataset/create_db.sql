CREATE TABLE kind (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind_name TEXT NOT NULL,
    food TEXT NOT NULL,
    noise TEXT NOT NULL
);

CREATE TABLE pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 0),
    kind_id INTEGER NOT NULL,
    owner TEXT NOT NULL,
    FOREIGN KEY (kind_id) REFERENCES kind(id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

INSERT INTO kind (kind_name, food, noise) 
VALUES ('Dog', 'Dog food', 'Bark');

INSERT INTO kind (kind_name, food, noise) 
VALUES ('Cat', 'Cat food', 'Meow');

INSERT INTO kind (kind_name, food, noise) 
VALUES ('Fish', 'Fish flakes', 'Blub');

INSERT INTO pets (name, age, kind_id, owner)
VALUES ('Suzy', 3, 1, 'Greg');  -- Dog

INSERT INTO pets (name, age, kind_id, owner)
VALUES ('Sandy', 2, 2, 'Steve');  -- Cat

INSERT INTO pets (name, age, kind_id, owner)
VALUES ('Dorothy', 1, 3, 'Elizabeth');  -- Fish

INSERT INTO pets (name, age, kind_id, owner)
VALUES ('Heidi', 4, 1, 'David');  -- Dog
