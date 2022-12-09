from fastapi import FastAPI, Path, Query, HTTPException, status, Body, Depends
from typing import Optional
from pydantic import BaseModel
from model import UserSchema, UserLoginSchema, DataAntrian
from auth.jwt_handler import signJWT
from auth.jwt_bearer import JWTBearer
import uvicorn
from database import database

app = FastAPI()

users = []

# pembuatan fungsi-fungsi pengecekan
def check_user(data: UserLoginSchema):
    for user in users:
        if user.username == data.username and user.password == data.password:
            return True
        return False
def check_name(data: UserSchema):
    for user in users:
        if user.fullname == data.fullname:
            return True
        return False
def check_username(data: UserSchema):
    for user in users:
        if user.username == data.username:
            return True
        return False

# Root API, Menampilkan message selamat datang
@app.get("/")
def welcome():
        return {"Welcome!": "Selamat datang di aplikasi Antrian Rumah Sakit!"}

# User SignUp [Create a new user]
@app.post("/signup", tags=["User Account Management"])
def user_signup(user : UserSchema =Body(default=None)):
    if (check_name(user)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="fullname sudah ada!")
    if (check_username(user)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username sudah ada!")
    users.append(user)
    return signJWT(user.username)

# User Login
@app.post("/login", tags=["User Account Management"])
def user_login(user : UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.username)
    else:
        return {
            "Error": "Detail Login Salah!"
        }

# View Data
@app.get("/antrian", tags=["Database"])
def getAntrianData():
    data = database.getAllData()
    return data

# View specifik Data
@app.get("/antrian/{patient}", tags=["Database"])
def getSpecifikData(patient: str):
    if (database.checkNama(patient)):
        data = database.getData(patient)
        return data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nama Pasien tidak ada!")

# Insert Data
@app.post("/new-antrian", tags=["Database"], dependencies=[Depends(JWTBearer())])
def addNewAntrian(data: DataAntrian = Body(...)):
    database.insertData(data)
    return {"message": "Insert berhasil dilakukan"}

# Update specifik Data
@app.put("/update-antrian/{patient}", tags=["Database"], dependencies=[Depends(JWTBearer())])
def updateData(patient: str, cond: bool = Query(..., description="sudah masuk / belum? (True/False)")):
    if (database.checkNama(patient)):
        database.updateData(patient, cond)
        return {"message": "Update berhasil dilakukan"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nama Pasien tidak ada!")
    
# Delete specifik Data
@app.delete("/delete-item", tags=["Database"], dependencies=[Depends(JWTBearer())])
def delete_item(patient: str = Query(..., description="The name of the patient to delete")):
    if (database.checkNama(patient)):
        database.deleteData(patient)
        return {"message": "Delete berhasil dilakukan"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nama Pasien tidak ada!")

# Prediksi Waktu Menunggu
# asumsi table database merupakan urutan antrian dengan baris pertama merupakan orang pertama
# sehingga prediksi dihitung berdasarkan jumlah orang yang belum masuk dikali 10 menit
@app.get("/waktu-menunggu/{patient}", tags=["Prediction"])
def prediction(patient: str):
    if (database.checkNama(patient)):
        count = database.jumlahTungguOrang(patient)
        waktu = count * 10
        jam = waktu / 60
        return {"message": "waktu tunggu {} adalah {} menit atau {} jam".format(patient, waktu, jam)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nama Pasien tidak ada!")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)