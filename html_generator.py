def generate_html(results):
    with open('template.html', 'r', encoding='utf-8') as file:
        template = file.read()

    results_html = ''
    databases_found = set()

    for r in results:
        results_html += f'<div class="info-item" data-type="{r["type"]}">'
        if r["type"] == "eldent":
            results_html += f'<strong>База данных:</strong> ELDENT<br>'
            results_html += f'<strong>ФИО:</strong> {r["ФИО"]}<br>'
            results_html += f'<strong>Номер телефона:</strong> {r["Номер телефона"]}<br>'
            results_html += f'<strong>Эл. почта:</strong> {r["Эл. почта"]}<br>'
        elif r["type"] == "maxrealt":
            results_html += f'<strong>База данных:</strong> MaxRealt<br>'
            results_html += f'<strong>Номер:</strong> {r["Номер"]}<br>'
            results_html += f'<strong>Продажи:</strong> {r["Продажи"]}<br>'
        elif r["type"] == "agroserver":
            results_html += f'<strong>База данных:</strong> AgroServer<br>'
            results_html += f'<strong>Объявление:</strong> {r["Объявление"]}<br>'
            results_html += f'<strong>Адрес:</strong> {r["Адрес"]}<br>'
            results_html += f'<strong>ФИО:</strong> {r["ФИО"]}<br>'
            results_html += f'<strong>Телефон:</strong> {r["Телефон"]}<br>'
        elif r["type"] == "vk_parsing":
            results_html += f'<strong>База данных:</strong> VK Parsing Lost and Found<br>'
            results_html += f'<strong>Имя:</strong> {r["Имя"]}<br>'
            results_html += f'<strong>Ссылка ВК:</strong> <a href="{r["Ссылка ВК"]}" target="_blank">{r["Ссылка ВК"]}</a><br>'
            results_html += f'<strong>Телефон:</strong> {r["Телефон"]}<br>'
        elif r["type"] in ["food", "food_v2"]:
            db_name = "M-Food Level Kitchen" if r["type"] == "food" else "M-Food Level Kitchen V2"
            results_html += f'<strong>База данных:</strong> {db_name}<br>'
            results_html += f'<strong>Номер:</strong> {r["Номер"]}<br>'
            results_html += f'<strong>Дата/время:</strong> {r["Дата/время"]}<br>'
            results_html += f'<strong>Сумма:</strong> {r["Сумма"]} {r["Валюта"]}<br>'
            results_html += f'<strong>E-Mail:</strong> {r["E-Mail"]}<br>'
            results_html += f'<strong>Телефон:</strong> {r["Телефон"]}<br>'
            results_html += f'<strong>Имя:</strong> {r["Имя"]}<br>'
            results_html += f'<strong>Адрес:</strong> {r["Адрес"]}<br>'
        elif r["type"] == "mirtesen":
            results_html += f'<strong>База данных:</strong> Mirtesen<br>'
            results_html += f'<strong>Телефон:</strong> {r["Телефон"]}<br>'
            results_html += f'<strong>ФИО:</strong> {r["ФИО"]}<br>'
        elif r["type"] == "undatos":
            results_html += f'<strong>База данных:</strong> Undatos<br>'
            results_html += f'<strong>Имя:</strong> {r["name"]}<br>'
            results_html += f'<strong>Телефон:</strong> {r["phone"]}<br>'
        elif r["type"] == "unqaqos":
            results_html += f'<strong>База данных:</strong> Unqaqos<br>'
            results_html += f'<strong>Имя:</strong> {r["name"]}<br>'
            results_html += f'<strong>Телефон:</strong> {r["phone"]}<br>'

        results_html += '</div><br>'

        databases_found.add(r["type"])

    buttons_html = '<button class="db-btn" onclick="filterResults(\'all\')">Все базы</button>\n'
    if "eldent" in databases_found:
        buttons_html += '<button class="db-btn" onclick="filterResults(\'eldent\')">ELDENT</button>\n'
    if "maxrealt" in databases_found:
        buttons_html += '<button class="db-btn" onclick="filterResults(\'maxrealt\')">MaxRealt</button>\n'
    if "agroserver" in databases_found:
        buttons_html += '<button class="db-btn" onclick="filterResults(\'agroserver\')">AgroServer</button>\n'
    if "vk_parsing" in databases_found:
        buttons_html += '<button class="db-btn" onclick="filterResults(\'vk_parsing\')">VK Parsing</button>\n'
    if "food" in databases_found:
        buttons_html += '<button class="db-btn" onclick="filterResults(\'food\')">M-Food Level Kitchen</button>\n'
    if "food_v2" in databases_found:
        buttons_html += '<button class="db-btn" onclick="filterResults(\'food_v2\')">M-Food Level Kitchen V2</button>\n'
    if "mirtesen" in databases_found:
        buttons_html += '<button class="db-btn" onclick="filterResults(\'mirtesen\')">Mirtesen</button>\n'
    if "undatos" in databases_found:
        buttons_html += '<button class="db-btn" onclick="filterResults(\'undatos\')">Undatos</button>\n'
    if "undatos" in databases_found:
        buttons_html += '<button class="db-btn" onclick="filterResults(\'unqaqos\')">Unqaqos</button>\n'
    return template.replace('{{RESULTS}}', results_html).replace('{{BUTTONS}}', buttons_html)