from datetime import datetime, timedelta, date
import os

start = datetime.today().date()
end = date(2026,12,31)

totaldays = end - start

os.chdir("./AllFolders")
cdate = datetime.now()
for i in range(totaldays.days+1):
    cdate = start + timedelta(days=i)
    newdate = cdate.strftime("%d-%m-%Y")
    #print(newdate)
    #print(cdate)

    os.mkdir(f"{newdate}")    
    os.chdir(f"{newdate}")

    with open(f"{newdate}.txt", 'w') as f:
        f.write(f"File was created at {newdate}")
    with open(f"{newdate}.py", 'w') as f:
        f.write(f"File was created at {newdate}")
    with open(f"{newdate}.json", 'w') as f:
        f.write(f"File was created at {newdate}")

    os.chdir("../")
