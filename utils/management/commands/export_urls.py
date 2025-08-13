# utils/management/commands/export_urls.py
# Кастомная management-команда export_urls, которая будет пробегать по urlpatterns проекта и
# выгружать все эндпоинты в Markdown-файл endpoints.md и в endpoints.png.
# Установить библиотеку:
# pip install pillow
# Запустить команду в терминале для выполнения скрипта:
# python manage.py export_urls


from django.core.management.base import BaseCommand
from django.urls import get_resolver
import os
from PIL import Image, ImageDraw, ImageFont

class Command(BaseCommand):
    help = "Export all project URLs to a Markdown file and PNG with colored HTTP methods"

    # # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # # TXT export
    # def extract_urls(self, patterns, prefix=''):
    #     url_list = []
    #     for pattern in patterns:
    #         if hasattr(pattern, 'url_patterns'):
    #             url_list += self.extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
    #         else:
    #             url_list.append(prefix + str(pattern.pattern))
    #     return url_list
    #
    # def handle(self, *args, **kwargs):
    #     urls = get_resolver().url_patterns
    #     urls_list = self.extract_urls(urls)
    #
    #     file_path = os.path.join(os.getcwd(), "utils/endpoints.txt")
    #     with open(file_path, "w", encoding="utf-8") as f:
    #         for url in urls_list:
    #             f.write(url + "\n")
    #
    #     self.stdout.write(self.style.SUCCESS(f"URL-s are saved in {file_path}"))

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def handle(self, *args, **options):
        resolver = get_resolver()
        urls = resolver.url_patterns

        md_lines = ["# API Endpoints", ""]
        md_lines.append("| Method(s) | Path | View |")
        md_lines.append("|-----------|------|------|")

        table_rows = []

        # Цвета для методов
        method_colors = {
            "GET": "#2ecc71",     # зелёный
            "POST": "#f1c40f",    # жёлтый
            "PUT": "#3498db",     # синий
            "DELETE": "#e74c3c",  # красный
            "ANY": "#7f8c8d"      # серый
        }

        def colorize_md(methods):
            parts = methods.split(", ")
            return " ".join([f"<span style='color:{method_colors.get(m, '#7f8c8d')}'>{m}</span>" for m in parts])

        def extract_patterns(patterns, prefix=""):
            for p in patterns:
                if hasattr(p, 'url_patterns'):
                    extract_patterns(p.url_patterns, prefix + str(p.pattern))
                else:
                    path_str = f"{prefix}{p.pattern}"
                    if path_str.startswith("admin/"):
                        continue

                    methods = getattr(p.callback, 'actions', None)
                    if methods:
                        method_list = ", ".join(m.upper() for m in methods.keys())
                    else:
                        method_list = "ANY"

                    view_name = f"{p.callback.__module__}.{p.callback.__name__}"
                    md_lines.append(f"| {colorize_md(method_list)} | `{path_str}` | `{view_name}` |")
                    table_rows.append((method_list, path_str, view_name))

        extract_patterns(urls)

        # Markdown export
        output_md = os.path.join(os.getcwd(), "utils/endpoints.md")
        os.makedirs(os.path.dirname(output_md), exist_ok=True)
        with open(output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # PNG export
        headers = ("Method(s)", "Path", "View")
        font_path = "arial.ttf"         # Убедись, что файл шрифта доступен
        # font_path = "C:\\Windows\\Fonts\\arial.ttf"   # для Windows
        try:
            font = ImageFont.truetype(font_path, size=14)
            font_headers = ImageFont.truetype(font_path, size=18)
        except IOError:
            font = ImageFont.load_default()

        padding = 20
        row_height = 24

        temp_img = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(temp_img)

        def get_text_width(text):
            return draw.textbbox((0, 0), text, font=font)[2]

        col_widths = [
            max(get_text_width(r[0]) for r in table_rows + [headers]) + padding,
            max(get_text_width(r[1]) for r in table_rows + [headers]) + padding,
            max(get_text_width(r[2]) for r in table_rows + [headers]) + padding
        ]

        img_width = sum(col_widths) + padding * 2
        img_height = (len(table_rows) + 2) * row_height + padding * 2

        img = Image.new("RGB", (img_width, img_height), "#0D1117")      # #f9f9f9 - light
        draw = ImageDraw.Draw(img)

        # ----------------------------------------------------------------------------------
        # Заголовки
        y = padding
        x = padding
        for i, h in enumerate(headers):
            draw.text((x+5, y+3), h, fill="#f000f0", font=font_headers)
            x += col_widths[i]
        y += row_height

        # ----------------------------------------------------------------------------------
        # Строки
        for method_str, path_str, view_str in table_rows:
            x = padding
            # Метод(ы)
            methods = method_str.split(", ")
            method_x = x
            for m in methods:
                draw.text((method_x+5, y+5), m, fill=method_colors.get(m, "#7f8c8d"), font=font)   #
                method_x += get_text_width(m + " ")   # добавляем пробел для отступа

            x += col_widths[0]
            # Путь
            draw.text((x+5, y+5), path_str, fill="#92979E", font=font)
            x += col_widths[1]
            # View
            draw.text((x+5, y+5), view_str, fill="#92979E", font=font)
            y += row_height

        # ----------------------------------------------------------------------------------
        # Линии таблицы
        for i in range(len(table_rows) + 2):
            y_line = padding + i * row_height
            # Горизонтальные лини таблицы:
            draw.line([(padding, y_line), (img_width - padding, y_line)], fill="#1D2127", width=1)  # #1D2127

        x_line = padding
        for w in col_widths:
            x_line += w
            # Вертикальные линии талицы:
            draw.line([(x_line, padding), (x_line, img_height - padding)], fill="#0D1117", width=1) # #1D2127

        output_png = os.path.join(os.getcwd(), "utils/endpoints_dark.png")
        img.save(output_png, format="PNG", optimize=True)

        self.stdout.write(self.style.SUCCESS(f"✅ Endpoints exported to endpoints.txt, {output_md} and {output_png}"))
