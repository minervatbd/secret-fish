CREATE TABLE users (
    id_user bigint NOT NULL,
    id_server bigint NOT NULL,

    display_name varchar(32) NOT NULL,
    
    points int NOT NULL DEFAULT '0',
    identity varchar(32) NOT NULL DEFAULT '',
    dex_count int NOT NULL DEFAULT '0',

    PRIMARY KEY (id_user, id_server)
);

CREATE TABLE dex_entries (
    id_user bigint NOT NULL,
    id_server bigint NOT NULL,
	id_fish varchar(32) NOT NULL DEFAULT '',

    catch_count int NOT NULL DEFAULT '0',

	PRIMARY KEY (id_user, id_server, id_fish)
);

CREATE TABLE timelines (
    id_server bigint NOT NULL,
    time_lasttick int NOT NULL DEFAULT '0',
    clock int NOT NULL DEFAULT '0',
    weather varchar(32) NOT NULL DEFAULT 'nonplussed',
    day int NOT NULL DEFAULT '1',
    global_catch_count bigint NOT NULL DEFAULT '0',

    PRIMARY KEY (id_server)
);