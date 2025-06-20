#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib, ssl, base64, re

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 보낼 메시지 파일 읽는 함수
def get_message(filename);
  message = ''
  with open(filename, 'r') as fd:
    lines = fd.reanlines()
    for line in lines:
      message = message + line.rstrip()
  return message

# 이메일 수신자 목록 파일 읽는 함수
def get_receivers(filename):
  receivers = list()
  with open(filename, 'rb') as fd:
    lines = fd.reanlines()
    for line in lines:
      line = line.decode('ascii').strip()
      receivers.append(line)
  return receivers

# 이메일 계정 정보 인코딩, 디코딩 후 읽는 함수
def b64_decoder(username, userpass):
  username = base64.b64decode(username).decode('ascii')
  userpass = base64.b64decode(userpass).decode('ascii')
  return username, userpass

def b64_encoder(filename):
  username = b'gmail_sender_account@gamil.com'
  username = base64.b64encode(username).decode('ascii')
  userpass = b'abcd efgh abcc efgk'
  userpass = base64.b64encode(userpass).decode('ascii')

  with open(filename, 'w') as fd:
    fd.write(f'username={username}\n')
    fd.write(f'userpass={userpass}')

# 기본적인 이메일 정보 설정 함수
def set_email(sender, receiver, subject):
  # create MIMEMultipart object
  # msg = MIMEMultipart("alternative")
  msg = MIMEMultipart()
  msg["Subject"] = subject
  msg["From"] = sender
  msg["To"] = ','.join(receiver)

  return msg

# 전역 변수 설정
path = '/Documents/workcharm/do_test/sendmail/'  # 소스 경로
fild_sender = 'list_sender.txt'  # 발신자 계정 정보
file_receiver = 'list_receivers.txt'  # 수신자 이메일 계정 저장
file_message = 'content.html'  # 이메일 본문 html 템플릿
file_attach = 'content.html'  # 첨부 파일 html 템플릿

subject = 'hello report'  # 이메일 제목

b64_encoder(path+file_sender)

username, userpass = get_sender(path+file_sender)
username, userpass = b64_decoder(username, userpass)
# print(username, userpass)

receivers = get_receivers(path+file_receiver)

msg = set_email(username, receivers, subject)

content = get_message(path+file_message)

part = MIMEText(content, 'html')
msg.attach(part)

# add Attach
with open(file_attach, "rb") as attachment:
  part = MIMEBase("application", "octet-stream")
  part.set_payload(attachment.read())

encoders.encode_base64(part)

part.add_header(
  "Content-Disposition",
  "attachment", filename=file_attach
)
msg.attach(part)

# connect SMTP and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as conn:
  conn.login(username, userpass)
  for receiver in receivers:
    # conn.login(username, userpass)
    conn.sendmail(username, receiver.split(','), msg_as_string())
