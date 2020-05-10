class Config():
    def __init__(self):
        self.token = #BOT SECRET TOKEN
        self.id = #BOT ID
        self.debug = False
        self.command_message = "Utilisez ❌ pour quitter la réunion, 🛎️ pour notifier les participants et 💼 pour commencer une session de travail"
        self.reu_param_message = "Sélectionnez une durée (en heures) avec les flèches ⬅️ ➡️ puis validez ✅.\nPour l'instant: 1"
        self.reu_message = "Réunion commencée !\n Utilisez ❌ pour l'annuler et ⏱️ pour connaître le temps restant."

cfg = Config()
