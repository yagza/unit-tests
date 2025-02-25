# https://support.checkmarx.com/s/article/How-to-generate-a-new-CxSAST-scan-report-through-the-REST-API

import requests

# Конфигурация
checkmarx_url = "https://<checkmarx-url>"
username = "<your-username>"
password = "<your-password>"
client_secret = "<client-secret>"

# Аутентификация
auth_url = f"{checkmarx_url}/cxrestapi/auth/identity/connect/token"
auth_data = {
    "username": username,
    "password": password,
    "grant_type": "password",
    "scope": "sast_rest_api",
    "client_id": "resource_owner_client",
    "client_secret": client_secret
}
auth_response = requests.post(auth_url, data=auth_data)
access_token = auth_response.json().get("access_token")

if not access_token:
    print("Ошибка аутентификации")
    exit()

# Получение списка отчётов
reports_url = f"{checkmarx_url}/cxrestapi/reports/sastScan"
headers = {"Authorization": f"Bearer {access_token}"}
reports_response = requests.get(reports_url, headers=headers)

if reports_response.status_code != 200:
    print("Ошибка при получении списка отчётов")
    exit()

reports = reports_response.json()

# Фильтрация и выгрузка готовых отчётов
for report in reports:
    report_id = report.get("id")
    report_status = report.get("status", {}).get("name")

    if report_status == "Completed":
        print(f"Отчёт {report_id} готов к выгрузке")

        # Загрузка отчёта
        download_url = f"{checkmarx_url}/cxrestapi/reports/sastScan/{report_id}"
        download_response = requests.get(download_url, headers=headers)

        if download_response.status_code == 200:
            # Сохранение отчёта в файл
            file_name = f"report_{report_id}.pdf"
            with open(file_name, "wb") as file:
                file.write(download_response.content)
            print(f"Отчёт {report_id} сохранён как {file_name}")
        else:
            print(f"Ошибка при загрузке отчёта {report_id}")
    else:
        print(f"Отчёт {report_id} не готов (статус: {report_status})")
