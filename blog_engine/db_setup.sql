CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(30),
  display_name VARCHAR(60),
  password_digest VARCHAR(50),
  session_token VARCHAR(50)
);

CREATE TABLE posts(
  id INTEGER PRIMARY KEY,
  title VARCHAR(100),
  author_id INTEGER,
  body TEXT
);

CREATE TABLE comments(
  id INTEGER PRIMARY KEY,
  author VARCHAR(50),
  email VARCHAR(60),
  website VARCHAR(80),
  body TEXT,
  post_id INTEGER
);


INSERT INTO users (id, username, display_name, password_digest, session_token)
VALUES (1, "admin", "Administrator", "d033e22ae348aeb5660fc2140aec35850c4da997", '');
INSERT INTO users (id, username, display_name, password_digest, session_token)
VALUES (2, "ts", "Twilight Sparkle", "850b4d7aa8e83b4c8121be5e4ad86739cf73ca01", '');
INSERT INTO users (id, username, display_name, password_digest, session_token)
VALUES (3, "third", "Third User", "34fb3300b9a77bebdc988ec3edd0d4a6a42a26f9", '');


INSERT INTO posts (id, title, body, author_id)
VALUES (1, "The First Post",
"<p>This is the text of the first post!</p><p>In case you were wondering</p>", 1);
INSERT INTO posts (id, title, body, author_id)
VALUES (2, "I Used to Wonder",
"<p>&mdash;what friendship could be. Until you-all shared its magic with me!</p><ul><li>Big adventure</li> <li>tons of fun</li><li>a beautiful heart</li><li>more??</li></ul>", 2);
INSERT INTO posts (id, title, body, author_id)
VALUES (3, "The Third Post",
"<p>This is the text of the third post! Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.</p>", 3);

INSERT INTO comments (id, author, email, website, body, post_id)
VALUES (1, "Friend of the Blog", "test@example.com", "http://example.com/", "<p>I do not agree with you! Because reasons.</p>", 1);
INSERT INTO comments (id, author, email, website, body, post_id)
VALUES (2, "Another Commenter", "ac@example.com", "http://example.com/2", "<p>The previous commenter makes an astute point. Who can say but that we must disagree with the post? Because reasons.</p><p>Because reasons, indeed.</p>", 1);
