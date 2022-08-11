import csv


def csv_write(filename, header, data):
    try:
        with open(filename, 'w') as csv_file:
            # csv_writer = csv.writer(csv_file)
            # csv_writer.writerow(header)
            # csv_writer.writerows(data)
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()
            csv_writer.writerows(data)
    except (IOError, OSError) as csv_file_error:
        print("Unable to write the contents to csv file. Exception: {}".format(csv_file_error))


if __name__ == '__main__':
    header = ['name', 'age', 'gender']
    # data = [['Richard', 32, 'M'], ['Mumzil', 21, 'F'], ['Melinda', 25, 'F']]
    data = [{'name': 'Richard', 'age': 32, 'gender': 'M'},
            {'name': 'Mumzil', 'age': 21, 'gender': 'F'}, {'name': 'Melinda', 'age': 25, 'gender': 'F'}]
    filename = 'sample_output.csv'
    csv_write(filename, header, data)
