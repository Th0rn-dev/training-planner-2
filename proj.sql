CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role_id UUID REFERENCES roles(id)
);

CREATE TABLE categories (
	id uuid DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar(100) NOT NULL,
	parent_id uuid NULL,
	CONSTRAINT categories_pkey PRIMARY KEY (id),
	CONSTRAINT categories_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES categories(id)
);

CREATE TABLE cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    preview_image_url VARCHAR(255),
    video_url VARCHAR(255) NOT NULL,
    invisible bool DEFAULT false NOT NULL,
    category_id UUID REFERENCES categories(id)
);

CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    card_id UUID REFERENCES cards(id),
    comment TEXT
);

CREATE TABLE training_session (
    id UUID NOT NULL,
    created_at DATE NOT NULL,
    training_date DATE NOT NULL,
    description VARCHAR(1000),

    CONSTRAINT pk_training_session PRIMARY KEY (id)
);

CREATE TABLE training_action (
    id UUID NOT NULL,
    card_id UUID,
    duration BIGINT NOT NULL,
    training_session_id UUID NOT NULL,

    CONSTRAINT pk_training_action PRIMARY KEY (id),
    CONSTRAINT fk_training_action_card FOREIGN KEY (card_id) REFERENCES card(id),
    CONSTRAINT fk_training_action_training_session FOREIGN KEY (training_session_id) REFERENCES training_session(id)
);