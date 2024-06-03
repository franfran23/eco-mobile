import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Paramètres de connexion SMTP
smtp_server = 'smtp.gmail.com'
port = 587
sender_email = 'eiccovoit@gmail.com'
password = 'votre-mot-de-passe'

# Créez le message
message = MIMEMultipart()
message['Subject'] = 'Code de vérification'
message['From'] = sender_email
message['To'] = 'destinataire@example.com'

# Corps du message
text = 'Bonjour, ceci est un e-mail envoyé depuis Python.'
message.attach(MIMEText(text, 'plain'))

# Connectez-vous au serveur SMTP et envoyez l'e-mail
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls()  # Utilisez TLS pour une connexion sécurisée
    server.login(sender_email, password)
    server.sendmail(sender_email, 'destinataire@example.com', message.as_string())

print('E-mail envoyé avec succès !')