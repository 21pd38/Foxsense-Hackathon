from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import mysql.connector
from flask_session import Session

mydb = mysql.connector.connect(
    host='127.0.0.1',  
    user='root',  
    password='VamsKris@987',
    database='foxsense'
)

mycursor = mydb.cursor(buffered=True)