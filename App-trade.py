import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QMessageBox, QDialog
import ccxt


def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split(' = ')
            config[key] = value
    return config
    
class CustomDialog(QDialog):
    def __init__(self, title,  message):
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(300, 800, 600, 300)
        self.setStyleSheet("QDialog {border: 2px solid black;}")

        layout = QVBoxLayout()
        label = QLabel(message)
        layout.addWidget(label)

        self.setLayout(layout)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Crypto APP')
        self.setGeometry(300, 800, 600, 300)
        self.setStyleSheet("QMainWindow {border: 2px solid black;}")

        self.move(300, 800)

        self.button_connect = QPushButton('Connect to OKX', self)
        self.button_connect.setGeometry(200, 100, 200, 50)
        self.button_connect.clicked.connect(self.ConnectExchange)

        # Создаем кнопку для продажи монет
        self.button_sell = QPushButton('Продать все монеты', self)
        self.button_sell.setGeometry(50, 100, 200, 50)
        self.button_sell.hide()
        #layout.addWidget(self.button_sell)

        self.button_buy = QPushButton('Купить монеты', self)
        self.button_buy.setGeometry(350, 100, 200, 50)
        self.button_buy.hide()

    def ConnectExchange(self):
        try:
            config = read_config('config.txt')
            apikey = config.get('apikey')
            secretkey = config.get('secretkey')
            password = config.get('password')
            path_excel = config.get('path_to_excel')
            test = bool(config.get('test'))

            if apikey and secretkey:
                print('\nAPI data from the file "config.txt" was read correctly:')
                print(f'test = {test}')
                print("API Key:", apikey)
                print("Secret Key:", secretkey)
                print("Your password:", password)
                
                # Создаем объект биржи
                exchange = ccxt.okx({
                'apiKey': apikey,
                'secret': secretkey,
                'password': password,
                'enableRateLimit': True
                })
                
                if (test):
                    exchange.setSandboxMode(True)

                try:
                    balance = exchange.fetch_balance()  # Получаем статус биржи
                    
                    self.button_sell.show()
                    self.button_sell.clicked.connect(lambda: self.executeSellOrder(exchange))                                        

                except ccxt.AuthenticationError as e:
                    print(e)
                    dialog = CustomDialog('Authentication error', 'check that the API Key, Secret Key and password are correct')
                    sys.exit(dialog.exec())

                except Exception as e:
                    print(e)
                    dialog = CustomDialog('Error', 'Please check terminal for details')
                    sys.exit(dialog.exec())

            else:
                dialog = CustomDialog('Error','Failed to read API data from file "config.txt"')
                sys.exit(dialog.exec())  

            if path_excel:
                self.button_buy.show()
                self.button_buy.clicked.connect(lambda: self.executeBuyOrder(exchange, path_excel))
                self.button_connect.hide()
                print('\npath to excel file from the file "config.txt" was read correctly:')
                print("Path to file: ", path_excel)
                
            else:
                dialog = CustomDialog('Error','Failed to read path to excel file from "config.txt"')
                dialog.exec()

        except FileNotFoundError:
            dialog = CustomDialog('Error','File "config.txt" not found')
            sys.exit(dialog.exec())


    def executeSellOrder(self, exchange):


        balance = exchange.fetch_balance()

        # Продаем все монеты по рыночной цене
        s = ""
        exchange.options['createMarketBuyOrderRequiresPrice'] = False
        for symbol, amount in balance['total'].items():
            if amount > 0 and symbol != 'USDT':  # Продаем только те монеты, которые есть на балансе
                try:
                    order = exchange.createMarketSellOrder(symbol + '/USDT', amount)
                    s += f"Продано {symbol}: Количество - {order['amount']}\n"
                except ccxt.NetworkError as e:
                    print(e)
                    s += f"Error {symbol}: NetworkError"
                except ccxt.ExchangeError as e:
                    print(e)
                    s += f"Error {symbol}: ExchangeError"
                except Exception as e:
                    print(e)
                    s += f"Error {symbol}: Exception"
        dialog = CustomDialog('Report',s)
        dialog.exec()

    def read_excel_file(self, file_path):
        try:
            # Чтение Excel-файла
            df = pd.read_excel(file_path, header = None)

            # Первый столбец - имена монет, второй столбец - сумма закупки
            coins = df.iloc[:, 0].tolist()
            purchase_amounts = df.iloc[:, 1].tolist()

            # Вывод имен монет и сумм закупок
            print("\nИмена монет:", coins)
            print("Суммы закупок:", purchase_amounts)

            return coins, purchase_amounts

        except Exception as e:
            print(e)
            dialog = CustomDialog('Error','Ошибка при чтении Excel-файла\nПроверьте путь к файлу и тип файла')
            dialog.exec()
            return 0, 0

    def executeBuyOrder(self, exchange, file_path):

        coins, amounts = self.read_excel_file(file_path)
        s = ""
        if (coins != 0):
            for symbol, amount in zip(coins, amounts):
                if amount > 0:  # Проверка, что сумма покупки больше 0
                    try:
                        pair = symbol.upper() + '/USDT'
                        market_price = exchange.fetchTicker(pair)['last']  # Получаем текущую рыночную цену
                        quantity = amount / market_price 
                        order = exchange.create_market_buy_order(pair, quantity)
                        s += f"Куплено {symbol}  На сумму: {order['cost']} USDT\n"
                    except ccxt.NetworkError as e:
                        print(e)
                        s += f"Error {symbol}: NetworkError\n"
                    except ccxt.ExchangeError as e:
                        print(e)
                        s += f"Error {symbol}: ExchangeError\n"
                    except Exception as e:
                        print(e)
                        s += f"Error {symbol}: Exception\n"
            dialog = CustomDialog('Report',s)
            dialog.exec()

    


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())