import os
import pandas as pd

MAX_TABLE_VALUE = 10
ESCAPE_PHRASE = 'exit'
MENU_URL = 'menu.csv'


def main():
    create_tables_directory()
    while True:
        table_number = validate_table_number(MAX_TABLE_VALUE)
        restaurant_table_object = TableObject(table_number)
        restaurant_table_object.action_handler()

def create_tables_directory():
    """
    Creates a 'table' directory if it doesn't already exit.
    """
    if not os.path.exists('tables'):
        os.mkdir('tables')


def validate_table_number(max_table_number: int) -> str:
    """
    Returns a valid integer as a string.
    :param max_table_number:
    :return: table_number
    :rtype: str
    """
    while True:
        table_number: str = input(f'Enter the Table Number (1 to {max_table_number}), or "{ESCAPE_PHRASE}" to end: ')
        if table_number.isdigit():
            if 1 <= int(table_number) <= max_table_number:
                return str(table_number)
        elif table_number == ESCAPE_PHRASE:
            exit()


class TableObject:
    def __init__(self, table_number):
        self.csv_url = 'tables/table' + table_number + '.csv'
        self.___create_csv_file()

    def ___create_csv_file(self):
        """
        Creates a corresponding csv file if it doesn't already exist.
        """
        if not os.path.exists(self.csv_url):
            with open(self.csv_url, 'x') as new_file:
                new_file.write('Item,Price')

    def action_handler(self):
        """
        Public method to access other private methods.
        """
        while True:
            choice = input(f'Enter an action (Append, Display, Clear), or "{ESCAPE_PHRASE}" to go back: ')
            if choice.lower() == ESCAPE_PHRASE:
                break

            if choice.lower().startswith('a'):  # append
                self.___append_new_items_into_a_dictionary()

            elif choice.lower().startswith('d'):  # display
                self.___display_csv_file_contents()

            elif choice.lower().startswith('c'):  # clear
                self.___clear_contents()

    def ___append_new_items_into_a_dictionary(self):
        print(menu := pd.read_csv(MENU_URL))
        items_to_append: dict = {'Item': [], 'Price': []}
        while True:
            desired_item = input(f'Enter an item from the menu, or "{ESCAPE_PHRASE}" to go back: ')
            if desired_item == ESCAPE_PHRASE:
                break

            query_result = menu[menu['Item'] == desired_item]
            if query_result.empty:
                print('Item not recognised')
                continue

            for _ in range(self.___append_get_quantity()):
                items_to_append['Item'].append(query_result.values[0][0])
                items_to_append['Price'].append(query_result.values[0][1])
        self.___append_update_csv_file_with_new_items(items_to_append)

    @staticmethod
    def ___append_get_quantity() -> int:
        """
        Gets the user's desired quantity for one type of item on the menu.
        :return: quantity
        :rtype: int
        """
        while True:
            quantity = input("Enter Quantity (0 to cancel): ")
            if quantity.isdigit():
                return int(quantity)

    def ___append_update_csv_file_with_new_items(self, new_items):
        df_current_entries = pd.read_csv(self.csv_url)
        df_new_entries = pd.DataFrame(data=new_items)
        df_combined_entries = pd.concat([df_new_entries, df_current_entries], ignore_index=True)
        df_combined_entries.to_csv(self.csv_url, mode='w', index=False)

    def ___display_csv_file_contents(self):
        """
        Displays the contents of csv file, unless the file as no entries.
        """
        if (csv_contents := pd.read_csv(self.csv_url)).empty:
            print('This table has no ordered items!')
            return
        print(csv_contents)
        print(f'Total: {sum(csv_contents["Price"])}')

    def ___clear_contents(self):
        """
        Resets csv file to only its headers.
        """
        with open(self.csv_url, 'w') as new_file:
            new_file.write('Item,Price')


if __name__ == '__main__':
    main()
