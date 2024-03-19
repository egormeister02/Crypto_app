## Иструкция к использованию
1. Для начала необходимо ввести свои данные в файл `config.txt`.\
Он выглядит следующим образом:
    ```
    apikey = <your apikey>
    secretkey = <your secretkey>
    password = <your password>
    path_to_excel = <path to excel file>
    ```
    Соответственно введите вместо\
    `<your apikey>` ваш API ключ\
    `<your secretkey>` ваш секретный API ключ\
    `<your password>` секретную фразу которую вы вводили при создании API\
    `<path to excel file>` путь до excel файла

    Обратите внимаие, что если excel файл лежит в той же папке что и приложение, достаточно ввести только имя файла, в противном случае необходимо прописать полный путь.

    Не забудьте, что ваш API должен иметь разрешение на трейдинг!
2. Теперь можно запускать приложение, первый запуск рекомендуется проводить из командной строки, чтобы видеть отчет об ошибках, которые могут возникнуть.\
При запуске приложение появится окно с кнопкой `Connect to OKX`, нажмите её.

    Приложение попытается подключиться к бирже, если подключение пройдет успешно, в окне появятсе две кнопки: `Продать все монеты` и `Купить монеты`

    Первая, соответственно, продает все монеты, имеющиеся на балансе по рыночной цене. После выполнения действия появится окно с отчетом.

    Вторая читает excel файл и покупает монтеы, указанные в первом столбце на сумму в USDT, которая указана во втором столбце таблицы. После выполнения действия появится окно с отчетом.
---
## Возможные ошибки
1. #### `Authentication error`
    - Проверьте интернет соеденение
    - Проверьте что сайт `okx.com` доступен без использования Vpn
    - Проверьте правильность ввода ключей и секретной фразы
    - Убедитесь что вы не используете VPN
    - Проверьте, что IP адресс вашего устройства находится в списке разрешенных адресов для вашего API\
        (в зависимости от системы приложение может выходить в интернет с нестандартного IP адреса, тогда сообщение о несоответствии IP адреса появится в терминале. Скопируйте адресс из терминала и добавьте его в список разрешенных вашего API)
2. #### Пара слов об excel файле
    В первом столбце находятся имена закупаемых монет, внутри кода они приводятся к верхнему регистру (так выглядят обозначения тикеров на бирже)

    Если какую-то монету не удалось купить вы увидите сообщение об этом в отчете. Этому могут быть две причины:
    - Недостаточно средств для заключения сделки
    - Неправильно указано имя тикера

    Иногда на биржах используются спецэфические обозначения тикеров. Вам необходимо узнать корректое имя и вписать его в таблицу.