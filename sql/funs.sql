delimiter $$


drop function if exists fn_userid_to_unique_str;

create function fn_userid_to_unique_str(
    userid integer unsigned
)
returns varchar(32) 
begin
    declare ret varchar(32) default '';

    declare rand_ch char(1) default 'X';

    declare i, ret_str_len int default 0;
    declare last_num integer unsigned default 0;

    set i = userid;
    while i > 0 do
        set last_num = i mod 10;
        set i = i div 10;
        if last_num > 0 then
            set ret = concat(last_num, ret);
        else
            set rand_ch = substring('ABCDEFGHIJKLMNOPQRSTUVWXYZ', round(rand() * 25) + 1, 1);
            set ret = concat(rand_ch, ret);
        end if;
        set ret_str_len = ret_str_len + 1;
    end while;

    while ret_str_len < 8 do
        set rand_ch = substring('ABCDEFGHIJKLMNOPQRSTUVWXYZ', round(rand() * 25) + 1, 1);
        set ret = concat(rand_ch, ret);
        set ret_str_len = ret_str_len + 1;
    end while;

    return ret;
end$$





delimiter ;
