import sys
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from model import DataAntrian

engine = create_engine("sqlite:///database.db")
sesi = Session(engine)

# Database model
class Antrian_RS(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient: str
    sudah_masuk: bool

# View All Data
def getAllData():
    temp= select(Antrian_RS)
    viewData= sesi.exec(temp).all()
    return viewData

# View Specifik Data
def getData(patient: str):
    temp= select(Antrian_RS).where(Antrian_RS.patient == patient)
    viewData= sesi.exec(temp).first()
    return viewData

# Check Nama
def checkNama(patient: str):
    temp= select(Antrian_RS).where(Antrian_RS.patient == patient)
    viewData= sesi.exec(temp).first()
    if viewData is None:
        return False
    else:
        return True

# Insert data
def insertData(data: DataAntrian):
    newData = Antrian_RS(
        id= data.id,
        patient= data.patient,
        sudah_masuk= data.sudah_masuk
    )
    sesi.add(newData)
    sesi.commit()

# Delete Data
def deleteData(patient: str):
    temp= select(Antrian_RS).where(Antrian_RS.patient == patient)
    data= sesi.exec(temp).first()
    sesi.delete(data)
    sesi.commit()

# Update Data
def updateData(patient: str, cond: bool):
    temp= select(Antrian_RS).where(Antrian_RS.patient == patient)
    data= sesi.exec(temp).first()
    data.sudah_masuk = cond
    sesi.add(data)
    sesi.commit()
    sesi.refresh(data)

# For prediction
def jumlahTungguOrang(patient: str):
    temp= select(Antrian_RS)
    viewData= sesi.exec(temp).all()
    count = 0
    for user in viewData:
        if (user.patient == patient and user.sudah_masuk == False):
            break
        else:
            if (user.sudah_masuk == False):
                count += 1
    return count