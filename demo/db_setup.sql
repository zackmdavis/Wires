CREATE TABLE posts(
id INTEGER PRIMARY KEY,
title VARCHAR(100),
author_id INTEGER,
body TEXT);

CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(30),
  display_name VARCHAR(60),
  password_digest VARCHAR(30)
);

INSERT INTO users (id, username, display_name, password_digest)
VALUES (1, "admin", "Administrator", "d033e22ae348aeb5660fc2140aec35850c4da997");
INSERT INTO users (id, username, display_name, password_digest)
VALUES (2, "ts", "Twilight Sparkle", "c71744fb652817f7711fa3b7a8d7c152be1bcd54");

INSERT INTO posts (id, title, body, author_id)
VALUES (1, "The First Post",
"<p>This is the text of the first post!</p><p>In case you were wondering</p>", 1);
INSERT INTO posts (id, title, body, author_id)
VALUES (2, "I Used to Wonder",
"<p>&mdash;what friendship could be. Until you-all shared its magic with me!</p>", 2);
