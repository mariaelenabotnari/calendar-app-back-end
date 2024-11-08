CREATE TABLE eveniment (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	titlu VARCHAR NOT NULL,
	descriere TEXT NOT NULL,
	"data" DATE NOT NULL,
	ora TEXT NOT NULL,  
	tip TEXT CHECK(tip IN ('obligatoriu', 'opțional')) NOT NULL,
	loc_id INTEGER NOT NULL,
	organizator_id INTEGER NOT NULL,
	CONSTRAINT eveniment_loc_FK FOREIGN KEY (loc_id) REFERENCES loc(id),
	CONSTRAINT eveniment_organizator_FK FOREIGN KEY (organizator_id) REFERENCES organizator(id)
);

CREATE TABLE loc (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	raion VARCHAR,
	oras VARCHAR NOT NULL,
	strada VARCHAR NOT NULL
);

CREATE TABLE organizator (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	start_date DATE DEFAULT (current_date) NOT NULL,
	nume VARCHAR NOT NULL,
	domeniu VARCHAR
);
