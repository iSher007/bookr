import xlsxwriter


def create_workbook(filename):
    workbook = xlsxwriter.Workbook(filename)
    return workbook


def create_worksheet(workbook):
    worksheet = workbook.add_worksheet()
    return worksheet


def close_workbook(workbook):
    workbook.close()


def write_data(worksheet, data):
    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet.write(row, col, data[row][col])
    worksheet.write(len(data), 0, 'Avg. Age')
    avg_formula = "=AVERAGE(B{}:B{})".format(1, len(data))
    worksheet.write(len(data), 1, avg_formula)



if __name__ == '__main__':
    data = [['John Doe', 38], ['Adam Cuvver', 22], ['Stacy Martin', 28], ['Tom Harris', 42]]
    example_workbook = create_workbook('Example.xlsx')
    example_worksheet1 = create_worksheet(example_workbook)
    write_data(example_worksheet1, data)
    close_workbook(example_workbook)
