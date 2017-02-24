drop table if exists names;
CREATE TABLE names
(
    id INTEGER PRIMARY KEY,
    name_male TEXT,
    name_female TEXT,
    script_male TEXT,
    script_female TEXT,
    meaning TEXT,
    first_name INTEGER,
    second_name INTEGER,
    language TEXT,
    source TEXT,
    confirmation TEXT,
    popularity TEXT,
    note TEXT
);