# Author: Marcos Lopez
# send email via gmails smtp server using your credentials

import smtplib
from email.MIMEText import MIMEText

class sendEmailGmail:
  serverURL = ''
  subject = ''
  sender = ''
  subject = ''
  to = ''
  text = ''
  smtp_user = ''
  smtp_pass = ''

  logging = ''
  logfilename=''

  def logit(self, data):
    if self.logging == 'yes':
      fw=open(self.logfilename, 'a')
      fw.write(data)
      fw.write('\n# ==\n')
      fw.close()
    else:
      print data

  def mail(self):
    headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n\r\b" % ( \
        self.sender, self.to, self.subject)
    headers = "Subject: %s\n" % ( self.subject)
    message = headers + self.text

    mailserver = smtplib.SMTP(self.serverURL, 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(self.smtp_user, self.smtp_pass)
    msg = MIMEText('body')
    msg['Subject'] = self.subject
    msg['From'] = self.sender
    msg['Reply-to'] = self.sender
    msg['To'] = self.to
    
    mailserver.sendmail(
        self.sender,
        self.to,
        message,
    )
    # attempt to login

    mailserver.close()







