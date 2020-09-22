CREATE TABLE source_codes(
   source_code VARCHAR (64) PRIMARY KEY,
   description VARCHAR (256) NOT NULL,
   profile_image VARCHAR (256) NOT NULL,
   alt_image VARCHAR (256) NOT NULL,
   created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE posts(
   post_id serial PRIMARY KEY,
   ext_id VARCHAR (64) NOT NULL,
   title VARCHAR (64) NOT NULL,
   link VARCHAR (256) UNIQUE NOT NULL,
   image VARCHAR (256) NOT NULL,
   alt_image VARCHAR (256),
   source_code VARCHAR (64) REFERENCES source_codes(source_code) NOT NULL,
   created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
   UNIQUE (ext_id, source_code)
);

CREATE TABLE notifications(
   n_id serial PRIMARY KEY,
   device_token VARCHAR (256) NOT NULL,
   source_code VARCHAR (64) REFERENCES source_codes(source_code) NOT NULL,
   created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
   UNIQUE (device_token, source_code)
);

CREATE USER app WITH PASSWORD 'vh38pt94dx';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app;