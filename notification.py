from notifypy import Notify
notification =Notify()

#Titre de la fenêtre de notification
nottification.title="Eic-Covoit: Nouveau message"

#Message de la notification
notification.message="Vous avez reçu un nouveau message de la part de {{ user }}"

#Son de la notif
notification.audio="/static/sons/notif.wav"

#Envoyer la notification
notification.send()