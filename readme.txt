
Команды для ручной установки можно посмотреть в файлике AF4_conf.txt
Для автоматической установки: 
    1. Назначить адреса на кластерных интерфейсах нод типа такого: ifconfig <interface_name> up; ip a add <IP>/<netmask> dev <interface_name>
    2. Файлики inventory.yaml и playbook.yaml положить на первую базовую ноду
    3. Активировать виртуальную среду: source /opt/ptaf/pywsc/bin/activate 
    4. Проверить, что все узлы доступны по кластерным интерфейсам: ansible all -i ./inventory.yaml -m ping
    5. Запустить ансибл: ansible-playbook -i inventory.yaml playbook.yaml (ансибл )
    6. Деактивируем виртуальную среду: deactivate
    7. Profit!
Дальше запустить инфру, мониторинг и деплой:
    /var/pt/infra/current/install.sh
    /var/pt/infra/current/install.sh --action=add_monitoring
    /var/pt/ptaf-deploy/current/install.sh

Если установка завершилась без ошибок, то будет failed = 0
Подключаемся в UI под login/password - admin/positive и запрашиваем лицензию
    https://192.168.88.170
Grafana доступна по ссылке ниже, login/password - admin/admin
    https://192.168.88.170:3000
