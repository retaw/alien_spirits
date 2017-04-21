drop table if exists players;
create table players
(
    openid          varchar(32) not null,
    userid          integer unsigned auto_increment,
    unique_code     varchar(32) default '',
    refresh_counter integer default 0,
    power_deducted  integer default 0,
    extra_power     integer default 0,
    played_video_code_set integer unsigned default 0,
    refresh_uts     datetime default null,
    primary key (openid),
    key(userid)
) engine=InnoDB;


drop table if exists items_on_map;
create table items_on_map
(
    item_index  integer unsigned not null,
    ownerid     integer unsigned not null,
    itemid      integer unsigned not null,
    coord_lat   double  not null,
    coord_lng   double  not null,
    unique key(item_index, ownerid)
) engine=InnoDB;


drop table if exists items_captured;
create table items_captured
(
    itemid      integer unsigned not null, 
    ownerid     integer unsigned not null,
    num         integer unsigned not null,
    unique key(itemid, ownerid)
) engine=InnoDB;


drop table if exists award;
create table award
(
    userid      integer unsigned not null,
    award_type  integer unsigned not null,
    award_code  bigint  unsigned not null
) engine=InnoDB;


#select unique_code, itemid, num  where a.ownerid == b.ownerid;
