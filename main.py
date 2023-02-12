from fetch_data import fetch_data
from process_data import process_data
from add_coordinates import add_coordinates
from save_data import save_data


def main():
    df = fetch_data()
    df_price = process_data(df)
    df_price_coordinates = add_coordinates(df_price)
    save_data(df_price_coordinates)


if __name__ == '__main__':
    main()
