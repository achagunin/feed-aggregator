### Пример создания таблиц БД для приложения
***
* create table log_tab(
* id int auto_increment primary key,
* ts timestamp default current_timestamp,
* operation varchar(512) not null,
* url varchar(512) not null,
* ip varchar(39) not null,
* browser varchar(64) not null,
* os varchar(64) not null);
***
* create table users_tab(
* id int auto_increment primary key,
* login varchar(64) not null,
* password_hash varchar(128) not null);
***
* create table channel_tab(
* id int auto_increment primary key,
* ts timestamp default current_timestamp on update current_timestamp,
* url_channel_c varchar(512) not null,
* status_code int not null,
* length_content int not null,
* title_channel varchar(512) not null,
* url_site varchar(512) not null);
***
* create table rss_tab(
* id int auto_increment primary key,
* url_channel_r varchar(512) not null,
* title_item varchar(512) not null,
* summary_item varchar(10240) not null,
* url_item varchar(512) not null,
* published_item varchar(32) not null);
***
