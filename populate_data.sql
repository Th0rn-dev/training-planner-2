DELETE FROM comments;
DELETE FROM cards;
DELETE FROM categories;

INSERT INTO categories ("name")
VALUES ('Category 1');
INSERT INTO categories ("name")
VALUES ('Category 2');
INSERT INTO categories ("name")
VALUES ('Category 3');
INSERT INTO categories ("name", parent_id)
VALUES ('Subcategory', (select id from categories limit 1) );

INSERT INTO cards (title, video_url, category_id, invisible)
VALUES ('Card in Subcategory', '_', (select c.id
                                from categories as c
                                where c.name like 'Subc%'), false);