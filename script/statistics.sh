host=127.0.0.1
port=3306
username=water
password=111111
dbname=game_test

out_file=statistics.out

if [ $# -ge 1 ]; then
    out_file=$1
fi

if [ $# -ge 2 ]; then
    host=$2
fi

if [ $# -ge 3 ]; then
    port=$3
fi

if [ $# -ge 4 ]; then
    username=$4
fi

if [ $# -ge 5 ]; then
    password=$5
fi

if [ $# -ge 6 ]; then
    game_test=$6
fi


sql="select unique_code as code, openid, itemid, num as itemnum from players as a left join items_captured as b on a.userid = b.ownerid;"

suffix=`date +%Y%m%d%H%M%S`
#echo $suffix

#echo $out_file'.'$suffix

echo $sql | mysql -u$username -p$password -h$host -P$port $dbname >> $out_file'.'$suffix
    
