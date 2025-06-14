import pandas as pd

books=pd.read_excel('books_og.xlsx')
#print(books.head(3)) #here for checking

#- Remove columns that contain “internal” in their name.
ones_to_drop = [c for c in books.columns if 'internal' in c.lower()]
books.drop(columns=ones_to_drop, inplace=True)


#- Reformat author names so that they always start with a capital letter.
books['Name']= books['Name'].str.title()
books['Surname']= books['Surname'].str.title()

#print(books.head(3))  #here for checking

#- Remove records from publishers other than Penguin Random House or Random House, except for books by Stephen King.
filter_publisher= books[(books['Publisher'] == 'Penguin Random House') | (books['Publisher'] == 'Random House')]
filter_King=books[(books['Surname'] == 'King')]

result=pd.concat([filter_publisher, filter_King]).drop_duplicates()

#print(result)  #here for checking

#- Remove empty records.
result.dropna(how='all', inplace=True)

#print(result) #here for checking

#In the end i converted end product(the result idk what to call it) into a .xlsx file (i didnt re-write the old one for debuging purpouses)
result.to_excel("books.xlsx")


"""
                             *****TODO LIST*****
- Remove columns that contain “internal” in their name. 
- Reformat author names so that they always start with a capital letter. 
- Remove records from publishers other than Penguin Random House or Random House, except for books by Stephen King. 
- Remove empty records.
"""