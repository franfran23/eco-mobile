from notifypy import Notify

notification =Notify()

#Ico notification
notification.icon = "path/to/static/Images/logo.png"

#Titre de la fenêtre de notification
notification.title="Eic-Covoit: Nouveau message"

#Message de la notification
notification.message="Vous avez reçu un nouveau message de la part de {{ user }}"

#Son de la notif
notification.audio="path/to/static/sons/notif.wav"

#Envoyer la notification
notification.send()