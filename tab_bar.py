import os
from kitty.fast_data_types import Screen, get_options
from kitty.tab_bar import (
    DrawData,
    ExtraData,
    TabBarData,
    as_rgb,
)

opts = get_options()

LEFT_SEP = ""
RIGHT_SEP = ""

# Имена процессов и префиксов, которые нужно скрывать при закрузке
IGNORE_TITLES = {"bash", "zsh", "fish", "sh", "kitty"}

def get_clean_title(tab: TabBarData) -> str:
    title = tab.title.strip()
    
    # Если заголовок - это просто имя оболочки (которое мелькает в первую секунду)
    if title.lower() in IGNORE_TITLES:
        return "~"

    # Если в заголовке есть "user@host: ~/path"
    if ":" in title:
        title = title.split(":", 1)[1].strip()

    # Заменяем домашнюю директорию на ~
    home = os.path.expanduser("~")
    if title.startswith(home):
        title = title.replace(home, "~", 1)

    # Оставляем только имя текущей папки, если это длинный путь
    if "/" in title and title != "~":
        parts = [p for p in title.split("/") if p]
        if parts:
            title = parts[-1]

    return title if title else "~"

def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    if tab.is_active:
        bg_color = draw_data.active_bg
        fg_color = draw_data.active_fg
    else:
        bg_color = draw_data.inactive_bg
        fg_color = draw_data.inactive_fg

    tab_bg = as_rgb(int(bg_color))
    tab_fg = as_rgb(int(fg_color))
    default_bg = as_rgb(int(draw_data.default_bg))

    # 1. Левый скругленный край
    screen.cursor.fg = tab_bg
    screen.cursor.bg = default_bg
    screen.draw(LEFT_SEP)

    # 2. Текст вкладки
    screen.cursor.fg = tab_fg
    screen.cursor.bg = tab_bg
    screen.draw(" ")
    
    clean_title = get_clean_title(tab)
    if len(clean_title) > 20:
        clean_title = clean_title[:19] + "…"
        
    screen.draw(clean_title)
    screen.draw(" ")

    # 3. Правый скругленный край
    screen.cursor.fg = tab_bg
    screen.cursor.bg = default_bg
    screen.draw(RIGHT_SEP)

    # 4. Пробел между вкладками
    screen.cursor.fg = default_bg
    screen.cursor.bg = default_bg
    screen.draw(" ")

    return screen.cursor.x
