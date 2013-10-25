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
VALUES (2, "ts", "Twilight Sparkle", "850b4d7aa8e83b4c8121be5e4ad86739cf73ca01");
INSERT INTO users (id, username, display_name, password_digest)
VALUES (3, "third", "Third User", "34fb3300b9a77bebdc988ec3edd0d4a6a42a26f9");


INSERT INTO posts (id, title, body, author_id)
VALUES (1, "The First Post",
"<p>This is the text of the first post!</p><p>In case you were wondering</p>", 1);
INSERT INTO posts (id, title, body, author_id)
VALUES (2, "I Used to Wonder",
"<p>&mdash;what friendship could be. Until you-all shared its magic with me!</p><ul><li>Big adventure</li> <li>tons of fun</li><li>a beautiful heart</li><li>more??</li></ul>", 2);
INSERT INTO posts (id, title, body, author_id)
VALUES (3, "The Third Post",
"<p>This is the text of the third post! Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.</p>", 3);
