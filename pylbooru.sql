BEGIN TRANSACTION;
CREATE TABLE files(inode integer, filename text, mtime integer, exist integer);
CREATE TABLE tags(inode integer, type integer, value text, exist integer);
CREATE TABLE dirs(dirname text, mtime integer, exist integer);
COMMIT;
