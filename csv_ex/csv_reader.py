import csv


def read_csv(filename):
    try:
        with open(filename, newline='') as csv_file:
            # csv_reader = csv.reader(csv_file)
            csv_reader2 = csv.DictReader(csv_file)
            # for record in csv_reader:
            #     print(record)
            for record2 in csv_reader2:
                print(record2)
                # print(record2.get('stock_symbol'))
    except (IOError, OSError) as file_read_error:
        print("Unable to open the csv file. Exception: {}".format(file_read_error))


if __name__ == '__main__':
    read_csv('market_cap.csv')
