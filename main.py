import telebot
import requests
from io import StringIO
import csv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from html_generator import generate_html
from typing import Optional, List, Dict

# Константы
API_TOKEN = '7067233375:AAEVxtJ91HWZfpttqTouMjTzX8JePKE8HkI'
ENCRYPTED_GITHUB_TOKEN = 'ᠸᠹᡂ_ᡡᠹᡣᡡ4ᡇᠼᡑ02ᡔᡃᡏᡡ2ᡜᠽᡦ0ᡦᡢ0ᡕᡛ8ᡥᠸᡥ6ᠸ1ᡟ790ᠸ'
REPO_OWNER = 'rpfozzy'
REPO_NAME = 'data5'

# Инициализация бота
bot = telebot.TeleBot(API_TOKEN)
user_results = {}

class GitHubTokenHandler:
    def __init__(self, encrypted_token: str):
        self.encrypted_token = encrypted_token
        self._decrypted_token: Optional[str] = None
        
        self.reverse_cipher = {
            '᠀': 'а', '᠅': 'б', '᠆': 'в', '᠇': 'г', '᠈': 'д', '᠐': 'е', '᠑': 'ё',
            '᠒': 'ж', '᠓': 'з', '᠔': 'и', '᠕': 'й', '᠖': 'к', '᠗': 'л', '᠘': 'м',
            '᠙': 'н', 'ᠠ': 'о', 'ᠡ': 'п', 'ᠢ': 'р', 'ᠣ': 'с', 'ᠤ': 'т', 'ᠥ': 'у',
            'ᠦ': 'ф', 'ᠧ': 'х', 'ᠨ': 'ц', 'ᠩ': 'ч', 'ᠪ': 'ш', 'ᠫ': 'щ', 'ᠬ': 'ъ',
            'ᠭ': 'ы', 'ᠮ': 'ь', 'ᠯ': 'э', 'ᠰ': 'ю', 'ᠱ': 'я', 'ᠲ': 'a', 'ᠳ': 'b',
            'ᠴ': 'c', 'ᠵ': 'd', 'ᠶ': 'e', 'ᠷ': 'f', 'ᠸ': 'g', 'ᠹ': 'h', 'ᠺ': 'i',
            'ᠼ': 'j', 'ᠽ': 'k', 'ᠾ': 'l', 'ᠿ': 'm', 'ᡀ': 'n', 'ᡁ': 'o', 'ᡂ': 'p',
            'ᡃ': 'q', 'ᡄ': 'r', 'ᡅ': 's', 'ᡆ': 't', 'ᡇ': 'u', 'ᡈ': 'v', 'ᡉ': 'w',
            'ᡊ': 'x', 'ᡋ': 'y', 'ᡌ': 'z', 'ᡍ': 'A', 'ᡎ': 'B', 'ᡏ': 'C', 'ᡐ': 'D',
            'ᡑ': 'E', 'ᡒ': 'F', 'ᡓ': 'G', 'ᡔ': 'H', 'ᡕ': 'I', 'ᡖ': 'J', 'ᡗ': 'K',
            'ᡘ': 'L', 'ᡙ': 'M', 'ᡚ': 'N', 'ᡛ': 'O', 'ᡜ': 'P', 'ᡝ': 'Q', 'ᡞ': 'R',
            'ᡟ': 'S', 'ᡠ': 'T', 'ᡡ': 'U', 'ᡢ': 'V', 'ᡣ': 'W', 'ᡤ': 'X', 'ᡥ': 'Y',
            'ᡦ': 'Z'
        }
    
    def _decrypt(self, text: str) -> str:
        return ''.join(self.reverse_cipher.get(char, char) for char in text)
    
    def get_token(self) -> str:
        if self._decrypted_token is None:
            self._decrypted_token = self._decrypt(self.encrypted_token)
        return self._decrypted_token

class Database:
    def __init__(self, name: str, file_path: str, delimiter: str, search_columns: List[int], result_columns: Dict[int, str]):
        self.name = name
        self.file_path = file_path
        self.delimiter = delimiter
        self.search_columns = search_columns
        self.result_columns = result_columns

    def search(self, content: str, query: str) -> List[Dict[str, str]]:
        results = []
        reader = csv.reader(StringIO(content), delimiter=self.delimiter)
        next(reader, None)  # Skip header row
        for row in reader:
            if any(col < len(row) and query.lower() in str(row[col]).lower() for col in self.search_columns):
                result = {"type": self.name}
                for col, name in self.result_columns.items():
                    result[name] = row[col] if col < len(row) else 'Н/Д'
                results.append(result)
        return results

class GitHubService:
    def __init__(self, token_handler: GitHubTokenHandler, repo_owner: str, repo_name: str):
        self.token_handler = token_handler
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def get_file_content(self, file_path: str) -> Optional[str]:
        url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}'
        headers = {'Authorization': f'token {self.token_handler.get_token()}'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            content = response.json()
            file_content = requests.get(content['download_url']).text
            return file_content
        except requests.RequestException:
            return None

# Инициализация сервисов
github_token_handler = GitHubTokenHandler(ENCRYPTED_GITHUB_TOKEN)
github_service = GitHubService(github_token_handler, REPO_OWNER, REPO_NAME)

# Определение баз данных
databases = [
    Database("alkotestery ru", "alkotestery.csv", ',', [0, 1, 2], {0: "Телефон", 1: "Почта", 2: "Фио"}),
    Database("skipk01122022", "skipk01122022.csv", ';', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
             {0: "ФИО", 1: "Рег номер", 2: "Статус", 3: "Дата рождения", 4: "Место рождения", 
              5: "ИНН", 6: "СНИЛС", 7: "Почтовый адрес", 8: "Телефон", 9: "Почта", 10: "Ссылка"}),
    # ... остальные базы данных остаются без изменений ...
]

def format_result(result: Dict[str, str]) -> str:
    formatted = f"База данных: {result['type'].upper()}\n"
    for key, value in result.items():
        if key != 'type':
            formatted += f"{key}: {value}\n"
    return formatted.strip()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Введите номер телефона, фамилию, электронную почту или адрес для поиска информации во всех базах данных.")

@bot.message_handler(func=lambda message: True)
def handle_query(message):
    query = message.text
    results = []

    for db in databases:
        content = github_service.get_file_content(db.file_path)
        if content:
            results.extend(db.search(content, query))

    if results:
        user_results[message.chat.id] = results
        for result in results:
            bot.reply_to(message, format_result(result))

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Создать HTML", callback_data="generate_html"))
        bot.send_message(message.chat.id, "Хотите создать HTML файл с результатами?", reply_markup=markup)
    else:
        bot.reply_to(message, "Ничего не найдено ни в одной из баз данных.")

@bot.callback_query_handler(func=lambda call: call.data == "generate_html")
def callback_generate_html(call):
    results = user_results.get(call.message.chat.id)
    
    if results:
        html_content = generate_html(results)
        bot.send_document(call.message.chat.id, ('result.html', html_content))
    else:
        bot.send_message(call.message.chat.id, "Нет данных для генерации HTML.")

if __name__ == '__main__':
    bot.polling(none_stop=True)
