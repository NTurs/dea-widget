// PWA установка
let deferredPrompt;

// Регистрация сервис-воркера
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => {
                console.log('Сервис-воркер зарегистрирован:', registration);
            })
            .catch(error => {
                console.error('Ошибка регистрации сервис-воркера:', error);
            });
    });
}

// Обработка установки PWA
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    // Показываем кнопку установки
    const installPrompt = document.getElementById('installPrompt');
    if (installPrompt) {
        installPrompt.classList.add('show');
    }
});

// Обработка успешной установки
window.addEventListener('appinstalled', () => {
    console.log('PWA установлено');
    const installPrompt = document.getElementById('installPrompt');
    if (installPrompt) {
        installPrompt.classList.remove('show');
    }
    deferredPrompt = null;
});

// Обработчики кнопок установки
document.addEventListener('DOMContentLoaded', () => {
    const installBtn = document.getElementById('installBtn');
    const closeBtn = document.getElementById('closeBtn');
    const installPrompt = document.getElementById('installPrompt');
    
    if (installBtn) {
        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                console.log('Результат установки:', outcome);
                deferredPrompt = null;
                installPrompt.classList.remove('show');
            }
        });
    }
    
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            installPrompt.classList.remove('show');
        });
    }
});

// Основная логика виджета
class DeAWidget {
    constructor() {
        this.timeElement = document.getElementById('time');
        this.dateElement = document.getElementById('date');
        this.phraseElement = document.getElementById('phrase');
        this.authorElement = document.getElementById('author');
        
        this.phrases = [
            { text: "Время — это то, что мы хотим больше всего, но используем хуже всего.", author: "Уильям Пенн" },
            { text: "Лучшее время для начала — сейчас.", author: "Неизвестный автор" },
            { text: "Каждая минута, потраченная на планирование, экономит пять минут на выполнение.", author: "Боб Проктор" },
            { text: "Время не ждет.", author: "Народная мудрость" },
            { text: "Успех — это лестница, по которой не взобраться, держа руки в карманах.", author: "Зиг Зиглар" },
            { text: "Действуй сейчас. Завтра может быть слишком поздно.", author: "Неизвестный автор" },
            { text: "Время — самый ценный капитал.", author: "Теодор Драйзер" },
            { text: "Не откладывай на завтра то, что можно сделать сегодня.", author: "Бенджамин Франклин" }
        ];
        
        this.currentPhraseIndex = 0;
        this.init();
    }
    
    init() {
        this.updateTime();
        this.updatePhrase();
        
        // Обновляем время каждую секунду
        setInterval(() => {
            this.updateTime();
        }, 1000);
        
        // Меняем фразу каждые 30 секунд
        setInterval(() => {
            this.updatePhrase();
        }, 30000);
    }
    
    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit'
        });
        const dateString = now.toLocaleDateString('ru-RU', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        if (this.timeElement) {
            this.timeElement.textContent = timeString;
        }
        if (this.dateElement) {
            this.dateElement.textContent = dateString;
        }
    }
    
    updatePhrase() {
        const phrase = this.phrases[this.currentPhraseIndex];
        
        if (this.phraseElement) {
            this.phraseElement.textContent = phrase.text;
        }
        if (this.authorElement) {
            this.authorElement.textContent = `— ${phrase.author}`;
        }
        
        // Переходим к следующей фразе
        this.currentPhraseIndex = (this.currentPhraseIndex + 1) % this.phrases.length;
    }
    
    // Получение фразы с сервера (если есть API)
    async getPhraseFromServer() {
        try {
            const response = await fetch('/api/phrase');
            if (response.ok) {
                const data = await response.json();
                return data;
            }
        } catch (error) {
            console.error('Ошибка получения фразы с сервера:', error);
        }
        return null;
    }
}

// Инициализация виджета
document.addEventListener('DOMContentLoaded', () => {
    new DeAWidget();
});

// Обработка офлайн/онлайн статуса
window.addEventListener('online', () => {
    console.log('Приложение онлайн');
    document.body.classList.remove('offline');
});

window.addEventListener('offline', () => {
    console.log('Приложение офлайн');
    document.body.classList.add('offline');
}); 