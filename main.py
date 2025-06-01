# Импорт необходимых библиотек
import pygame  # Основная библиотека для создания игры
import sys     # Для работы с системными функциями (выход из игры)

# Инициализация всех модулей Pygame
pygame.init()

# Константы игры
WIDTH, HEIGHT = 800, 600  # Ширина и высота игрового окна
FPS = 60                  # Количество кадров в секунду

# Цвета в формате RGB (Red, Green, Blue)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Загрузка графических ресурсов
# Фоновое изображение
background = pygame.image.load('assets/Cosmos.png')

# Словарь с изображениями планеты в разных состояниях
planet_images = {
    'bad': pygame.image.load('assets/Earth_Hottest.png'),    # Сильно загрязненная Земля
    'medium': pygame.image.load('assets/Earth_Hot.png'),     # Среднее состояние
    'good': pygame.image.load('assets/Earth.png')            # Чистая Земля
}

# Создание прямоугольника для позиционирования планеты по центру экрана
planet_rect = planet_images['bad'].get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Настройка игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна заданного размера
pygame.display.set_caption("Кликер Земля")        # Заголовок окна

# Объект для контроля частоты кадров
clock = pygame.time.Clock()

# Загрузка шрифтов разных размеров
font_small = pygame.font.SysFont(None, 30)   # Мелкий шрифт
font_medium = pygame.font.SysFont(None, 50)  # Средний шрифт
font_large = pygame.font.SysFont(None, 70)   # Крупный шрифт

# Состояния игры
MENU = 0   # Главное меню
GAME = 1   # Игровой процесс
WIN = 2    # Экран победы
game_state = MENU  # Текущее состояние игры (по умолчанию - меню)

# Игровые переменные
score = 0            # Текущее количество очков игрока
planet_stage = 'bad'  # Текущее состояние планеты (начинаем с плохого)
mnijitel = 1         # Множитель очков за клик (увеличивается при улучшениях)
win_count = 0        # Счетчик купленных улучшений (для определения победы)

# Система улучшений
# Каждое состояние планеты имеет свои уникальные улучшения
upgrades = {
    # Улучшения для плохого состояния планеты
    'bad': [
        {'name': 'Сажать деревья', 'cost': 30, 'bought': False},
        {'name': 'Запретить бензин', 'cost': 20, 'bought': False},
        {'name': 'Убрать озоновые дыры', 'cost': 40, 'bought': False},
    ],
    # Улучшения для среднего состояния
    'medium': [
        {'name': 'Переработка', 'cost': 70, 'bought': False},
        {'name': 'Чистая энергия', 'cost': 50, 'bought': False},
        {'name': 'Образование', 'cost': 90, 'bought': False},
    ],
    # Улучшения для хорошего состояния
    'good': [
        {'name': 'Вывоз воды с земли в космос', 'cost': 100, 'bought': False},
        {'name': 'Глобальное сотрудничество', 'cost': 150, 'bought': False},
        {'name': 'Зеленые города', 'cost': 180, 'bought': False},
    ]
}

# Проблемные изображения, которые отображаются на планете, пока улучшение не куплено
problem_images = {
    'bad': [
        pygame.image.load('assets/upgrades/problem_trees.png'),    # Проблема деревьев
        pygame.image.load('assets/upgrades/problem_benzin.png'),  # Проблема бензина
        pygame.image.load('assets/upgrades/problem_ozon.png'),    # Проблема озона
    ],
    'medium': [
        pygame.image.load('assets/upgrades/problem_recycle.png'), # Проблема переработки
        pygame.image.load('assets/upgrades/problem_energy.png'),  # Проблема энергии
    ],
    'good': [
        pygame.image.load('assets/upgrades/problem_water.png'),  # Проблема воды
    ]
}

def draw_text(text, font, color, pos, centered=False):
    """
    Функция для отрисовки текста на экране
    :param text: Текст для отображения
    :param font: Шрифт для текста
    :param color: Цвет текста
    :param pos: Позиция текста (x, y)
    :param centered: Если True, текст будет центрирован относительно pos
    """
    img = font.render(text, True, color)  # Создаем изображение текста
    if centered:
        # Корректируем позицию для центрирования
        pos = (pos[0] - img.get_width() // 2, pos[1] - img.get_height() // 2)
    screen.blit(img, pos)  # Отрисовываем текст на экране

def create_button(text, font, color, bg_color, rect, hover_color=None):
    """
    Функция создания и отрисовки кнопки
    :param text: Текст на кнопке
    :param font: Шрифт текста
    :param color: Цвет текста
    :param bg_color: Цвет фона кнопки
    :param rect: Прямоугольник кнопки (x, y, width, height)
    :param hover_color: Цвет кнопки при наведении (опционально)
    :return: Возвращает False, так как клики обрабатываются в основном цикле
    """
    mouse_pos = pygame.mouse.get_pos()
    
    # Проверка наведения курсора на кнопку
    if rect.collidepoint(mouse_pos):
        if hover_color:
            # Рисуем кнопку с цветом наведения
            pygame.draw.rect(screen, hover_color, rect, border_radius=10)
    else:
        # Рисуем кнопку с обычным цветом
        pygame.draw.rect(screen, bg_color, rect, border_radius=10)
    
    # Отрисовываем текст кнопки по центру
    draw_text(text, font, color, (rect.x + rect.width // 2, rect.y + rect.height // 2), True)
    
    return False  # Клики обрабатываются отдельно в основном цикле

def update_planet_stage():
    """
    Обновляет состояние планеты, когда все улучшения текущей стадии куплены
    """
    global planet_stage, mnijitel, win_count
    current_upgrades = upgrades[planet_stage]
    
    # Проверяем, все ли улучшения куплены
    if all(u['bought'] for u in current_upgrades):
        win_count += len(current_upgrades)  # Увеличиваем счетчик улучшений
        
        # Переход на следующую стадию
        if planet_stage == 'bad':
            mnijitel = 5       # Увеличиваем множитель очков
            planet_stage = 'medium'  # Переходим на среднюю стадию
        elif planet_stage == 'medium':
            mnijitel = 10      # Еще увеличиваем множитель
            planet_stage = 'good'   # Переходим на хорошую стадию

def reset_game():
    """
    Сбрасывает все игровые параметры для начала новой игры
    """
    global score, planet_stage, mnijitel, win_count, game_state, upgrades
    
    # Сброс основных переменных
    score = 0
    planet_stage = 'bad'
    mnijitel = 1
    win_count = 0
    
    # Сброс всех улучшений (отмечаем как некупленные)
    for stage in upgrades:
        for upgrade in upgrades[stage]:
            upgrade['bought'] = False
    
    game_state = GAME  # Переходим в игровой режим

# Основной игровой цикл
running = True  # Флаг работы игры
while running:
    clock.tick(FPS)  # Контроль частоты кадров
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если закрыли окно
            running = False  # Завершаем игру
        
        # Обработка кликов левой кнопкой мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()  # Получаем позицию клика
            
            if game_state == MENU:  # Если в главном меню
                # Проверка клика по кнопке "Начать игру"
                start_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
                if start_button.collidepoint(mouse_pos):
                    reset_game()  # Начинаем новую игру
                
                # Проверка клика по кнопке "Выход"
                exit_button = pygame.Rect(WIDTH // 2 - 100, 370, 200, 50)
                if exit_button.collidepoint(mouse_pos):
                    running = False  # Завершаем игру
            
            elif game_state == GAME:  # Если в игровом режиме
                # Клик по планете - добавляем очки
                if planet_rect.collidepoint(mouse_pos):
                    score += mnijitel
                
                # Проверка кликов по улучшениям
                current_upgrades = upgrades[planet_stage]
                for i, upgrade in enumerate(current_upgrades):
                    # Создаем прямоугольник для зоны клика улучшения
                    text_rect = pygame.Rect(15, 500 + i * 30, 400, 30)
                    if text_rect.collidepoint(mouse_pos):
                        # Если улучшение не куплено и хватает очков
                        if not upgrade['bought'] and score >= upgrade['cost']:
                            score -= upgrade['cost']  # Вычитаем стоимость
                            upgrade['bought'] = True  # Отмечаем как купленное
                            update_planet_stage()     # Проверяем переход на след. стадию
            
            elif game_state == WIN:  # Если на экране победы
                # Кнопка "В меню"
                menu_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
                if menu_button.collidepoint(mouse_pos):
                    game_state = MENU  # Возвращаемся в меню
                
                # Кнопка "Выход"
                exit_button = pygame.Rect(WIDTH // 2 - 100, 370, 200, 50)
                if exit_button.collidepoint(mouse_pos):
                    running = False  # Завершаем игру
    
    # Отрисовка фона
    screen.blit(background, (0, 0))
    
    # Отрисовка в зависимости от состояния игры
    if game_state == MENU:  # Главное меню
        # Заголовок игры
        draw_text("КЛИКЕР ЗЕМЛЯ", font_large, WHITE, (WIDTH // 2, 150), True)
        # Подзаголовок
        draw_text("Спаси планету от глобального потепления!", font_medium, WHITE, (WIDTH // 2, 220), True)
        
        # Кнопка "Начать игру"
        start_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
        create_button("Начать игру", font_medium, BLACK, GREEN, start_button, (100, 255, 100))
        
        # Кнопка "Выход"
        exit_button = pygame.Rect(WIDTH // 2 - 100, 370, 200, 50)
        create_button("Выход", font_medium, WHITE, RED, exit_button, (200, 0, 0))
    
    elif game_state == GAME:  # Игровой процесс
        # Отрисовка планеты (текущего состояния)
        screen.blit(planet_images[planet_stage], planet_rect)

        # Отрисовка проблемных изображений (если улучшение не куплено)
        problem_imgs = problem_images.get(planet_stage, [])
        current_upgrades = upgrades[planet_stage]
        for i in range(len(problem_imgs)):
            upgrade = current_upgrades[i]
            if not upgrade['bought']:  # Если улучшение не куплено
                problem_img = problem_imgs[i]
                problem_rect = problem_img.get_rect(center=planet_rect.center)
                screen.blit(problem_img, problem_rect)

        # Отрисовка текущего счета
        draw_text(f"Очки: {score}", font_small, WHITE, (370, 45))

        # Отрисовка доступных улучшений для текущей стадии
        for i, upgrade in enumerate(current_upgrades):
            # Зеленый цвет для купленных, белый - для доступных
            color = GREEN if upgrade['bought'] else WHITE
            text = f"{upgrade['name']} - {upgrade['cost']} очков"
            draw_text(text, font_small, color, (15, 500 + i * 30))
        
        # Проверка условия победы (куплены все улучшения)
        if win_count >= 9:
            game_state = WIN  # Переходим на экран победы
    
    elif game_state == WIN:  # Экран победы
        # Большая надпись "ПОБЕДА!"
        draw_text("ПОБЕДА!", font_large, GREEN, (WIDTH // 2, 150), True)
        # Поздравление
        draw_text("Вы спасли планету от глобального потепления!", font_medium, WHITE, (WIDTH // 2, 220), True)
        
        # Кнопка "В меню"
        menu_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
        create_button("В меню", font_medium, BLACK, GREEN, menu_button, (100, 255, 100))
        
        # Кнопка "Выход"
        exit_button = pygame.Rect(WIDTH // 2 - 100, 370, 200, 50)
        create_button("Выход", font_medium, WHITE, RED, exit_button, (200, 0, 0))
    
    # Обновление экрана
    pygame.display.flip()

# Завершение игры
pygame.quit()  # Деинициализация Pygame
sys.exit()     # Выход из программы