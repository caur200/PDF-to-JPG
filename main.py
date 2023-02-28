import fitz
import os
import PySimpleGUI as sg

# Определяем элементы графического интерфейса
layout = [
    [sg.Text("Каталог с исходными файлами:"), sg.Input(key="input_dir"), sg.FolderBrowse()],
    [sg.Text("Каталог с конечными результатами:"), sg.Input(key="output_dir"), sg.FolderBrowse()],
    [sg.Button("Конвертировать"), sg.Button("Выход"), sg.Button("О программе")]
]

# Создаем окно из элементов
window = sg.Window("P2J", layout, icon='P2J.ico')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Выход":
        break
    elif event == "Конвертировать":
        input_dir = values["input_dir"]
        output_dir = values["output_dir"]

        # Создаем папку для конечных файлов, если она не существует
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Проходим по всем PDF-файлам в указанном каталоге
        for filename in os.listdir(input_dir):
            if filename.endswith(".pdf"):
                # Открываем PDF-файл
                with fitz.open(os.path.join(input_dir, filename)) as pdf:
                    # Конвертируем каждую страницу PDF в отдельный JPG-файл
                    for i, page in enumerate(pdf):
                        # Получаем пиксельное представление страницы в виде картинки
                        transform = fitz.Matrix(1, 1).prerotate(0)
                        pixmap = page.get_pixmap(matrix=transform, dpi=300, alpha=False)

                        # Создаем имя выходного файла
                        output_filename = f"{os.path.splitext(filename)[0]}_{i+1}.jpg"
                        # Сохраняем JPG-файл в указанном каталоге
                        pixmap.save(os.path.join(output_dir, output_filename))

        sg.popup("Конвертация завершена")
        window["input_dir"].update("")
        window["output_dir"].update("")

    elif event == "О программе":
        sg.popup("PDF в JPG конвертер", "Версия 1.0", "Автор: Артур Хидиров", "2023 год")
window.close()
