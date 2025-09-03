#!/bin/bash

# Скрипт запуска Telegram-бота

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Проверка наличия Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker не установлен. Установите Docker сначала."
        exit 1
    fi
}

# Проверка наличия .env файла
check_env_file() {
    if [ ! -f .env ]; then
        print_error "Файл .env не найден!"
        print_warning "Создайте файл .env на основе .env.example"
        print_warning "cp .env.example .env"
        print_warning "И отредактируйте значения"
        exit 1
    fi
}

# Сборка Docker образа
build_image() {
    print_status "Сборка Docker образа..."
    docker build -t salary-bot .
}

# Запуск контейнера
run_container() {
    print_status "Запуск бота..."
    docker run -d \
        --name salary-bot \
        --restart unless-stopped \
        --env-file .env \
        salary-bot
}

# Остановка и удаление старого контейнера
cleanup() {
    print_status "Остановка старого контейнера..."
    docker stop salary-bot 2>/dev/null || true
    docker rm salary-bot 2>/dev/null || true
}

# Показать текущие настройки
show_settings() {
    if [ -f .env ]; then
        print_status "Текущие настройки из .env:"
        echo "------------------------------------------"
        grep -E '^(BOT_TOKEN|MY_SALARY|PARTNER_SALARY)=' .env | while read line; do
            if [[ $line == BOT_TOKEN* ]]; then
                echo "BOT_TOKEN=*** (скрыто)"
            else
                echo "$line"
            fi
        done
        echo "------------------------------------------"
    fi
}

# Основная функция
main() {
    print_status "Запуск Telegram-бота для расчета взносов"
    echo "=========================================="

    check_docker
    check_env_file
    show_settings
    cleanup
    build_image
    run_container

    print_status "Бот успешно запущен!"
    print_status "Для просмотра логов: docker logs salary-bot"
    print_status "Для остановки: docker stop salary-bot"
}

# Запуск основной функции
main "$@"