import os
import pandas


MAX_TABLE_VALUE = 10
ESCAPE_PHRASE = 'exit'
MENU_URL = 'menu.csv'

if not os.path.exists('tables'):
    os.mkdir('tables')
while True:
    while True:
        table_number: str = input(f'Enter the Table Number (1 to {MAX_TABLE_VALUE}), or "{ESCAPE_PHRASE}" to end: ')
        if table_number.isdigit():
            if 1 <= int(table_number) <= MAX_TABLE_VALUE:
                csv_url = 'tables/table' + table_number + '.csv'
                if not os.path.exists(csv_url):
                    with open(csv_url, 'x') as new_file:
                        new_file.write('Item,Price')

                while True:
                    choice = input(f'Enter an action (Append, Display, Clear), or "{ESCAPE_PHRASE}" to go back: ')
                    if choice == ESCAPE_PHRASE:
                        break

                    if choice == 'Append':
                        print(menu := pandas.read_csv(MENU_URL))
                        items_to_append: dict = {'Item': [], 'Price': []}
                        while True:
                            desired_item = input(
                                f'Enter an item from the menu, or "{ESCAPE_PHRASE}" to go back: ')
                            if desired_item == ESCAPE_PHRASE:
                                break

                            query_result = menu[menu['Item'] == desired_item]
                            if query_result.empty:
                                print('Item not recognised')
                                continue

                            while True:
                                quantity = input("Enter Quantity (0 to cancel): ")
                                if quantity.isdigit():
                                    break
                            for _ in range(int(quantity)):
                                items_to_append['Item'].append(query_result.values[0][0])
                                items_to_append['Price'].append(query_result.values[0][1])

                            df_current_entries = pandas.read_csv(csv_url)
                            df_new_entries = pandas.DataFrame(data=items_to_append)

                            df_combined_entries = pandas.concat([df_new_entries, df_current_entries],ignore_index=True)
                            df_combined_entries.to_csv(csv_url, mode='w',index=False)

                    elif choice == 'Display':
                        if (csv_contents := pandas.read_csv(csv_url)).empty:
                            print('This table has no ordered items!')

                        else:
                            print(csv_contents)
                            print(f'Total: {sum(csv_contents["Price"])}')

                    elif choice == 'Clear':
                        with open(csv_url, 'w') as new_file:
                            new_file.write('Item,Price')
        elif table_number == ESCAPE_PHRASE:
            exit()