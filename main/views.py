import os

from django.conf import settings
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Homage - Главная страница'
        context['title_page'] = 'HOMAGE'
        context['subtitle'] = '— интернет-магазин\nуходовой и декоративной косметики'
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Homage - о нас'
        context['content'] = 'Об этом проекте'
        file_path = os.path.join(settings.BASE_DIR, 'static', 'deps', 'txt', 'about_this_project.txt')
        with open(file_path, encoding='utf-8', mode='r') as f:
            file_content = f.read()
        context['text_on_page'] = file_content
        return context


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Homage - контакты'
        context['content'] = 'Контакты'
        context['contacts'] = {
            'github': 'https://github.com/AxoLena',
            'telegram': '@hiiirch',
            'email': 'alena.sukhar333@gmail.com'
        }
        return context