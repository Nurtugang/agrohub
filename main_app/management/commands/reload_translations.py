# Для продакшна
# В локалхосте все работает без этого, но продакшне нужно перезагружать WSGI после обновления переводов
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Compile translations and reload WSGI'
    
    def handle(self, *args, **options):
        # Компилируем переводы
        os.system('python manage.py compilemessages')
        
        # Touch wsgi.py для перезагрузки
        wsgi_path = '/var/www/agrohub/agrohub/wsgi.py'
        os.utime(wsgi_path, None)
        
        self.stdout.write(self.style.SUCCESS('Переводы обновлены и WSGI перезагружен!'))