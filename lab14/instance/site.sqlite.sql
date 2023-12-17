BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "todo" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(100),
	"description"	VARCHAR(200),
	"complete"	BOOLEAN,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(20) NOT NULL,
	"email"	VARCHAR(120) NOT NULL,
	"image_file"	VARCHAR(20) NOT NULL,
	"password_hash"	VARCHAR(60) NOT NULL,
	UNIQUE("username"),
	UNIQUE("email"),
	PRIMARY KEY("id")
);
INSERT INTO "alembic_version" VALUES ('438356f0bf70');
INSERT INTO "user" VALUES (3,'Oleh','mypost@gmail.com','','55555');
INSERT INTO "user" VALUES (4,'user1','user1@example.com',' ','new_hash');
INSERT INTO "user" VALUES (5,'user2','user2@example.com',' ','hash2');
INSERT INTO "user" VALUES (6,'user3','user3@example.com',' ','hash3');
INSERT INTO "user" VALUES (7,'user','zarembovskabohdana@gmail.com','default.jpg','$2b$12$LrhrE6kAmDepAqmgPLbLTO7QxZPd0ZRPRCyRbs.DjmH57Go1bPt8O');
INSERT INTO "user" VALUES (8,'user123','user123@gmail.com','image.png','$2b$12$3I9y/bmzQ8uGRQfPdiYNk.tRe11ABuY7mbSXv55Mtsw1ZFLzH3a8u');
INSERT INTO "user" VALUES (9,'user5','user5@lol.com','image.png','$2b$12$h949Gs0fyN/diLk5C.aykecn3SI.JpjVTDAplJ85/8PbVirPIZ4sm');
INSERT INTO "user" VALUES (10,'Dana','zarembovskabohdana1@gmail.com','image.png','$2b$12$HVzy7TrFMobv8CtuXCifnORFS8t0NlQGaLAO28Z10drm0JefkpUm6');
COMMIT;
