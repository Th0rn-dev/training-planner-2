DELETE FROM comments;
DELETE FROM cards;
DELETE FROM categories;
DELETE FROM training_action;
DELETE FROM training_session;

INSERT INTO categories ("name")
VALUES ('Category 1');
INSERT INTO categories ("name")
VALUES ('Category 2');
INSERT INTO categories ("name")
VALUES ('Category 3');
INSERT INTO categories ("name", parent_id)
VALUES ('Subcategory', (select id from categories limit 1) );

INSERT INTO cards (title, video_url, category_id, invisible)
VALUES ('Card in Subcategory', '_', (SELECT c.id
                                FROM categories AS c
                                WHERE c.name LIKE 'Subc%'), false);

INSERT INTO training_session(id, created_at, training_date, description)
VALUES (gen_random_uuid(), now(), now(), 'first training session');

INSERT INTO training_action(id, duration, training_session_id)
VALUES (gen_random_uuid(), 1000, (SELECT id FROM training_session LIMIT 1));