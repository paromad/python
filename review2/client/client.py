import requests
import argparse


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=8000, type=int)

    return parser


def graceful_exit():
    ack = input("Are you sure you want to leave (Y/N)?")
    if ack == "Y":
        print("Goodbye!")
        exit()
    elif ack == "N":
        print("OK, let's continue")
    else:
        print("Incorrect command")
        graceful_exit()


def existing_commands():
    print(
        "Existing commands:\n"
        "put money,\n"
        "quantity of money\n"
        "get stocks\n"
        "get prices\n"
        "buy stocks\n"
        "sell stocks\n"
        "exit"
    )


def get_amount():
    amount = input("How much do you want to put? ")

    try:
        amount = int(amount)
    except ValueError:
        print("Incorrect amount")
        return 0

    if amount < 0:
        print("Incorrect amount")
        return 0
    return amount


def quantity_of_money(main_args):
    money = requests.get(
        f"http://{main_args.host}:{main_args.port}/quantity_of_money"
    ).text
    print(f"Now you have {money}")


def put_money(main_args):
    amount = get_amount()

    money = requests.post(
        f"http://{main_args.host}:{main_args.port}/put_money",
        params=dict(amount=amount),
    ).text
    print(f"Now you have {money} coins")


def print_dict(dictionary):
    print("Now you have:")
    for item in dictionary:
        print(f"{item} : {dictionary[item]}")


def get_stocks(main_args):
    stocks = requests.get(f"http://{main_args.host}:{main_args.port}/get_stocks").json()
    print("Now you have:")
    print_dict(stocks)
    return stocks


def get_prices(main_args):
    prices = requests.get(f"http://{main_args.host}:{main_args.port}/get_prices").json()
    print("Prices now:")
    print_dict(prices)
    return prices


def operation_with_stock(main_args, command, stocks):
    stock = input(f"What do you want to {command}? ")
    if stock not in stocks:
        print("Incorrect stock")
        return
    amount = get_amount()

    res = requests.post(
        f"http://{main_args.host}:{main_args.port}/{command}_stocks",
        params=dict(stock=stock, amount=amount),
    ).text
    print(res)


def buy_stocks(main_args):
    stocks = get_prices(main_args)
    operation_with_stock(main_args, "buy", stocks)


def sell_stocks(main_args):
    get_prices(main_args)
    stocks = get_stocks(main_args)
    operation_with_stock(main_args, "sell", stocks)


def main():
    main_parser = create_main_parser()
    main_args = main_parser.parse_args()

    while True:
        try:
            cmd = input("Enter command > ")
            if cmd == "help":
                existing_commands()
            elif cmd == "put money":
                put_money(main_args)
            elif cmd == "quantity of money":
                quantity_of_money(main_args)
            elif cmd == "get stocks":
                get_stocks(main_args)
            elif cmd == "get prices":
                get_prices(main_args)
            elif cmd == "buy stocks":
                buy_stocks(main_args)
            elif cmd == "sell stocks":
                sell_stocks(main_args)
            elif cmd == "exit":
                graceful_exit()
            else:
                print("Incorrect command, write \"help\" to see possible commands")
        except KeyboardInterrupt:
            graceful_exit()


if __name__ == "__main__":
    main()
