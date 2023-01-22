Обеспечение работы нового сайта
===============================
## Необходимые пакеты:
* nginx
* Python 3.10
* virtualenv + pip
* Git

например, в Ubuntu:
    sudo apt-get install nginx git python310 python3.10-env

## Конфигурация виртуального узла Nginx

* см. nginx.template.conf
* заменить SITENAME, например, на staging.my-domen.com

## Служба Systemd

* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на staging.my-domen.com
* заменить SEKRIT на почтовый пароль

## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username

/home/username
﹂ sites
   ﹂ SITENAME
      ⊢ database
      ⊢ source
      ⊢ static
      ﹂ virtualenv
