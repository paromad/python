import requests
import argparse


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=8000, type=int)

    return parser


def graceful_exit():
    ack = input("Are you sure you want to leave (Y/N)? ").strip()
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
        "put money\n"
        "quantity of money\n"
        "get my stocks\n"
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


def server_request(request):
    def wrapper(main_args, command, dictionary={}):
        try:
            return request(main_args, command, dictionary)
        except requests.exceptions.ConnectionError:
            print("Sorry, server is not working now")
            exit()

    return wrapper


@server_request
def get_request(main_args, command, dictionary={}):
    return requests.get(
        f"http://{main_args.host}:{main_args.port}/{command}", params=dictionary,
    )


@server_request
def post_request(main_args, command, dictionary):
    return requests.post(
        f"http://{main_args.host}:{main_args.port}/{command}", params=dictionary,
    )


def quantity_of_money(main_args):
    money = get_request(main_args, "quantity_of_money").text
    print(f"Now you have {money} coins")


def put_money(main_args):
    amount = get_amount()

    money = post_request(main_args, "put_money", dict(amount=amount)).text
    print(f"Now you have {money} coins")


def print_dict(dictionary):
    if len(dictionary) == 0:
        print("Nothing :(")
    for item in dictionary:
        print(f"{item} : {dictionary[item]}")


def get_my_stocks(main_args):
    stocks = get_request(main_args, "get_my_stocks").json()
    print("Now you have:")
    print_dict(stocks)
    return stocks


def get_prices(main_args):
    prices = get_request(main_args, "get_prices").json()
    print("Prices now:")
    print_dict(prices)
    return prices


def operation_with_stock(main_args, command, stocks):
    stock = " ".join(input(f"What do you want to {command}? ").split())
    if stock not in stocks:
        print("Incorrect stock")
        return
    amount = get_amount()

    res = post_request(
        main_args, f"{command}_stocks", dict(stock=stock, amount=amount)
    ).text
    if res == "Failed":
        if command == "buy":
            print("Sorry, you have not enough money")
        else:
            print(f"Sorry, you have not enough {stock}")
    else:
        print(res)
        get_my_stocks(main_args)


def buy_stocks(main_args):
    stocks = get_prices(main_args)
    operation_with_stock(main_args, "buy", stocks)


def sell_stocks(main_args):
    get_prices(main_args)
    stocks = get_my_stocks(main_args)
    operation_with_stock(main_args, "sell", stocks)


def main():
    main_parser = create_main_parser()
    main_args = main_parser.parse_args()

    while True:
        try:
            cmd = " ".join(input("Enter command > ").split())
            if cmd == "help":
                existing_commands()
            elif cmd == "put money":
                put_money(main_args)
            elif cmd == "quantity of money":
                quantity_of_money(main_args)
            elif cmd == "get my stocks":
                get_my_stocks(main_args)
            elif cmd == "get prices":
                get_prices(main_args)
            elif cmd == "buy stocks":
                buy_stocks(main_args)
            elif cmd == "sell stocks":
                sell_stocks(main_args)
            elif cmd == "exit":
                graceful_exit()
            else:
                print('Incorrect command, write "help" to see possible commands')
        except KeyboardInterrupt:
            graceful_exit()


if __name__ == "__main__":
    main()
