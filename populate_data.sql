INSERT INTO public.categories ("name") VALUES('Соуфа');
INSERT INTO public.categories ("name") VALUES('Формы');
INSERT INTO public.categories ("name") VALUES('Чисао');

INSERT INTO public.cards (title, category_id)
VALUES('Название карточки', (select id from categories limit 1 ));