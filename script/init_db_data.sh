
username=water
password=111111

host=127.0.0.1

dbname=game_test

table_def_file=../sql/tables.sql
fun_def_file=../sql/funs.sql

cat $table_def_file | mysql -u$username -p$password -h$host $dbname

echo "show tables" | mysql -u$username -p$password -h$host $dbname

cat $fun_def_file  | mysql -u$username -p$password -h$host $dbname


echo "------------Done---------"
