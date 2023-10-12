# Service_Book_PyQt5
Εφαρμογή αποθήκευσης ιστορικού συντήρησης Η/Υ και μηχανών γραφείου και 
Διαχείριση αποθήκης ανταλλακτικών και αναλώσιμων


Χρειάζεται το  arabic_reshaper φακελο απο το site_packages  να είναι στο ιδιο φακελο με το exe 
γιατι κατι τρεχει με το pyinstaller και δεν το βαζει

Για δημιουργία pdf αρχείων
Δεν μπορούν τα windows να ανοίξουν το προσωρινό Font 
reportlab.pdfbase.ttfonts.TTFError: Can't open file "C:\Users\dannys\AppData\Local\Temp\tmpokjxtzo7.ttf"

the temp solution is (tested on python 3.11 windows 11 xhtml2pdf==0.2.8 )
file:
Python311\site-packages\xhtml2pdf\context.py line 853
file = TTFont(fullFontName, filename)
change it to
file = TTFont(fullFontName, file.uri)
in this way going to use the same ttf file and not copy it to temp folder

![Preview](https://github.com/dannyswolf/Service_Book_PyQt5/blob/master/Screenshot%202021-11-27%20174248.png)
