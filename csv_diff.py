import csv
with open('path1', 'rb') as csvfile1:
    with open ("path2", "rb") as csvfile2:
        reader1 = csv.reader(csvfile1)
        reader2 = csv.reader(csvfile2)
        rowsCurrent = {row[0]:row for row in reader1} #file1 row dict
        rowsUpdated = [row for row in reader2] #file2 row list
        diffList = []
        for row in rowsUpdated:
            if row[0] in rowsCurrent and rowsCurrent[row[0]] != row:
                diffList.append(row)
        print len(diffList)
        with open('/Users/ian/Desktop/diffedCSV.csv', 'wb') as diffFile:
            writer = csv.writer(diffFile)
            writer.writerows(diffList)
