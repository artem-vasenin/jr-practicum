from dotenv import load_dotenv
import os

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
PROXY_API_TOKEN = os.getenv("PROXY_API_TOKEN")
PROXY_API = os.getenv("PROXY_API")

IMG = {
    'gpt': 'AgACAgIAAxkBAAILg2e60X46FBRho_EO760le4r55V0fAAKO8jEbkrLQSaNJrChaWS1YAQADAgADeAADNgQ',
    'quiz': 'AgACAgIAAxkBAAILhGe60b5aQtFBRKeHfY2j-8Y1AAFY4gACqugxG3v72EmtZjzKY8Ip9AEAAwIAA3gAAzYE',
    'random': 'AgACAgIAAxkBAAILhWe60dhf9ZkeTOAea8-3HdPy3iRYAAKQ8jEbkrLQSX1-KJ6tKY_fAQADAgADeQADNgQ',
    'talk': 'AgACAgIAAxkBAAILhme60fbI1Embhat4dZjW-FDOCxMqAAKR8jEbkrLQSWhyA6cRoh2NAQADAgADeAADNgQ',
    'talk_cobain': 'AgACAgIAAxkBAAILh2e60iHxKjdoJhavFwUmDfffEsSWAAKT8jEbkrLQSU0mRC08mVciAQADAgADeAADNgQ',
    'talk_hawking': 'AgACAgIAAxkBAAILiGe60ki24-kv4oZMZZK_qAufBcTwAAKW8jEbkrLQSX1N7CDexrfHAQADAgADeQADNgQ',
    'talk_nietzsche': 'AgACAgIAAxkBAAILiWe60msElp7mjdlZormmNuo930ErAAKf8jEbkrLQSUmLj_EhW36KAQADAgADeQADNgQ',
    'talk_queen': 'AgACAgIAAxkBAAILime60pFshCsbDhxbN3pwkEvzKu-JAALC8jEbkrLQSYnmSSAu8kLLAQADAgADeQADNgQ',
    'talk_tolkien': 'AgACAgIAAxkBAAILi2e60sp5IoVHs6plG1zzqpJMYoZmAAKv6DEbe_vYSesPA7rvTipOAQADAgADeQADNgQ',
}