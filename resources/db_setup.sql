CREATE TABLE source_codes(
   source_code VARCHAR (64) PRIMARY KEY,
   description VARCHAR (256) NOT NULL,
   created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE posts(
   post_id serial PRIMARY KEY,
   ext_id VARCHAR (64) NOT NULL,
   title VARCHAR (64) NOT NULL,
   link VARCHAR (256) UNIQUE NOT NULL,
   source_code VARCHAR (64) REFERENCES source_codes(source_code) NOT NULL,
   created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
   UNIQUE (ext_id, source_code)
);

INSERT INTO source_codes
VALUES ('minecraft_snapshot', 'Minecraft snapchot blog', DEFAULT),
       ('dayz', 'Dayz blog', DEFAULT),
       ('gen_zero', 'Minecraft snapchot blog', DEFAULT);

CREATE USER app WITH PASSWORD 'vh38pt94dx';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app;