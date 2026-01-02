import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service pour l'envoi d'emails"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
        self.from_name = settings.FROM_NAME
    
    def _send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Envoie un email
        
        Args:
            to_email: Email du destinataire
            subject: Sujet de l'email
            html_content: Contenu HTML de l'email
            text_content: Contenu texte alternatif (optionnel)
        
        Returns:
            True si l'email a été envoyé, False sinon
        """
        try:
            # Créer le message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email
            
            # Ajouter le contenu texte (fallback)
            if text_content:
                part1 = MIMEText(text_content, "plain", "utf-8")
                message.attach(part1)
            
            # Ajouter le contenu HTML
            part2 = MIMEText(html_content, "html", "utf-8")
            message.attach(part2)
            
            # Envoyer l'email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)
            
            logger.info(f"Email envoyé avec succès à {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email à {to_email}: {str(e)}")
            return False
    
    def send_verification_code(
        self,
        to_email: str,
        prenom: str,
        code: str
    ) -> bool:
        """
        Envoie le code de vérification pour l'inscription
        
        Args:
            to_email: Email du destinataire
            prenom: Prénom de l'utilisateur
            code: Code de vérification à 6 chiffres
        
        Returns:
            True si l'email a été envoyé, False sinon
        """
        subject = "Vérifiez votre adresse email"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .code-box {{
                    background-color: #fff;
                    border: 2px dashed #4CAF50;
                    padding: 20px;
                    text-align: center;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .code {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #4CAF50;
                    letter-spacing: 5px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📚 Bibliothèque en Ligne</h1>
                </div>
                <div class="content">
                    <h2>Bonjour {prenom} !</h2>
                    <p>Merci de vous être inscrit à notre bibliothèque en ligne.</p>
                    <p>Pour finaliser votre inscription, veuillez utiliser le code de vérification ci-dessous :</p>
                    
                    <div class="code-box">
                        <div class="code">{code}</div>
                    </div>
                    
                    <p>Ce code est valide pendant 15 minutes.</p>
                    <p>Si vous n'avez pas demandé cette inscription, vous pouvez ignorer cet email.</p>
                    
                    <p>À bientôt sur notre plateforme !</p>
                    <p><strong>L'équipe Bibliothèque en Ligne</strong></p>
                </div>
                <div class="footer">
                    <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Bonjour {prenom} !
        
        Merci de vous être inscrit à notre bibliothèque en ligne.
        
        Pour finaliser votre inscription, veuillez utiliser le code de vérification suivant :
        
        {code}
        
        Ce code est valide pendant 15 minutes.
        
        Si vous n'avez pas demandé cette inscription, vous pouvez ignorer cet email.
        
        À bientôt sur notre plateforme !
        L'équipe Bibliothèque en Ligne
        """
        
        return self._send_email(to_email, subject, html_content, text_content)
    
    def send_welcome_email(
        self,
        to_email: str,
        prenom: str
    ) -> bool:
        """
        Envoie un email de bienvenue après vérification
        
        Args:
            to_email: Email du destinataire
            prenom: Prénom de l'utilisateur
        
        Returns:
            True si l'email a été envoyé, False sinon
        """
        subject = "Bienvenue sur notre bibliothèque en ligne !"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .feature {{
                    background-color: #fff;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #4CAF50;
                }}
                .button {{
                    display: inline-block;
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Bienvenue {prenom} !</h1>
                </div>
                <div class="content">
                    <p>Votre compte a été créé avec succès !</p>
                    <p>Vous pouvez maintenant profiter de toutes les fonctionnalités de notre bibliothèque en ligne :</p>
                    
                    <div class="feature">
                        <strong>📖 Consulter le catalogue</strong><br>
                        Parcourez notre collection de livres numériques
                    </div>
                    
                    <div class="feature">
                        <strong>💾 Emprunter des livres</strong><br>
                        Empruntez vos livres préférés en quelques clics
                    </div>
                    
                    <div class="feature">
                        <strong>📝 Demander des transcriptions</strong><br>
                        Demandez la transcription de documents selon vos besoins
                    </div>
                    
                    <div class="feature">
                        <strong>👤 Gérer votre profil</strong><br>
                        Personnalisez votre expérience utilisateur
                    </div>
                    
                    <center>
                        <a href="{settings.FRONTEND_URL}" class="button">Accéder à la bibliothèque</a>
                    </center>
                    
                    <p>Si vous avez des questions, n'hésitez pas à nous contacter.</p>
                    <p>Bonne lecture !</p>
                    <p><strong>L'équipe Bibliothèque en Ligne</strong></p>
                </div>
                <div class="footer">
                    <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Bienvenue {prenom} !
        
        Votre compte a été créé avec succès !
        
        Vous pouvez maintenant profiter de toutes les fonctionnalités de notre bibliothèque en ligne :
        
        - Consulter le catalogue de livres numériques
        - Emprunter des livres en quelques clics
        - Demander des transcriptions de documents
        - Gérer votre profil personnel
        
        Accédez à la bibliothèque : {settings.FRONTEND_URL}
        
        Si vous avez des questions, n'hésitez pas à nous contacter.
        
        Bonne lecture !
        L'équipe Bibliothèque en Ligne
        """
        
        return self._send_email(to_email, subject, html_content, text_content)
    
    def send_password_reset(
        self,
        to_email: str,
        prenom: str,
        reset_token: str
    ) -> bool:
        """
        Envoie un email de réinitialisation de mot de passe
        
        Args:
            to_email: Email du destinataire
            prenom: Prénom de l'utilisateur
            reset_token: Token de réinitialisation
        
        Returns:
            True si l'email a été envoyé, False sinon
        """
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        subject = "Réinitialisation de votre mot de passe"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #FF9800;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .button {{
                    display: inline-block;
                    background-color: #FF9800;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left: 4px solid #FF9800;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔒 Réinitialisation du mot de passe</h1>
                </div>
                <div class="content">
                    <h2>Bonjour {prenom},</h2>
                    <p>Nous avons reçu une demande de réinitialisation de mot de passe pour votre compte.</p>
                    
                    <center>
                        <a href="{reset_url}" class="button">Réinitialiser mon mot de passe</a>
                    </center>
                    
                    <div class="warning">
                        <strong>⚠️ Important :</strong><br>
                        Ce lien est valide pendant 1 heure seulement.<br>
                        Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
                    </div>
                    
                    <p>Pour votre sécurité, ne partagez jamais ce lien avec personne.</p>
                    
                    <p>Cordialement,</p>
                    <p><strong>L'équipe Bibliothèque en Ligne</strong></p>
                </div>
                <div class="footer">
                    <p>Cet email a été envoyé automatiquement, merci de ne pas y répondre.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Bonjour {prenom},
        
        Nous avons reçu une demande de réinitialisation de mot de passe pour votre compte.
        
        Cliquez sur le lien suivant pour réinitialiser votre mot de passe :
        {reset_url}
        
        ⚠️ IMPORTANT :
        Ce lien est valide pendant 1 heure seulement.
        Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
        
        Pour votre sécurité, ne partagez jamais ce lien avec personne.
        
        Cordialement,
        L'équipe Bibliothèque en Ligne
        """
        
        return self._send_email(to_email, subject, html_content, text_content)


# Instance singleton du service
email_service = EmailService()