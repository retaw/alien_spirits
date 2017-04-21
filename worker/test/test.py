import json


class C:
    def f0(self):
        self.a = 2
    def f1(self):
        self.f0()
        print self.a



c = C()
c.f1()


d0 = {
        "userid": 101,
        "refresh_counter_day": 2,
        "items": [(1, ("11", 111)), (2, (22, 222))],
        }
s = json.dumps(d0)
print s

d1 = json.loads(s)
print d1

#
#sql = """
#INSERT INTO tablename (tag) SELECT $tag FROM (select 1) as tb WHERE NOT EXISTS( SELECT tag FROM tablename WHERE tag = $tag) LIMIT 1
#"""
#insert into players (openid) select "dj8" from (select 1) as tb where not exist(select openid from players where openid = "dj8") limit 1
#
#
#
#
#INSERT INTO your_table (`id`,`val`) VALUES(1,'Foo') ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(`id`);
#
#SELECT LAST_INSERT_ID();
#
#
#insert into players (userid, openid) values("dj8") on duplicate key update userid=last_insert_id()
#
#insert into players (userid) values('dj8') on duplicate key
#
