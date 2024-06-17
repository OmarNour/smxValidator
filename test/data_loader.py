from excel_reader.data_loader import Excel

if __name__ == '__main__':
    excel = Excel()
    excel.parse_file("C:\\Users\\on250000\\Documents\\Book1.xlsx")
    print(excel.data)
