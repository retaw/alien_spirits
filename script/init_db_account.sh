#!/bin/bash

host=127.0.0.1
root_pwd=111111


username=water
password=111111

dbname=game_test

echo "grant usage on *.* to '$username'@'%';" | mysql -uroot -h$host -p$root_pwd


echo "drop user '$username'; flush privileges;" | mysql -uroot -h$host -p$root_pwd


echo "create user $username identified by '$password';"  | mysql -uroot -h$host -p$root_pwd

#
echo "create database if not exists $dbname;" | mysql -uroot -h$host -p$root_pwd

#
echo "grant all privileges on $dbname.* to '$username'@'%' identified by '$password';"
echo "grant all privileges on $dbname.* to '$username'@'%' identified by '$password';" | mysql -uroot -h$host -p$root_pwd

#
#echo "grant all on $dbname.* to '$username'@'%';" | mysql -uroot -h$host -p$root_pwd

#
echo "flush privileges;" | mysql -uroot -h$host -p$root_pwd


