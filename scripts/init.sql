CREATE DATABASE email_sender;

\c email_sender

CREATE TABLE emails (
    id serial not null,
    date timestamp not null default current_timestamp,
    subject varchar(100) not null,
    message varchar(250) not null
);