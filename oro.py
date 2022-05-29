from datetime import datetime
print(datetime.today().strftime('%A, %B %d, %Y %H:%M:%S'))
print(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
meca = 19100
dosnet = 18500
nivek2 = 15100
total = meca + dosnet + nivek2
print ('Oro total acumulado :', total)
total = total*0.95
print ('Oro total que llegaria :', total)
print (total*0.00086, "$/G")
