from django.views.generic import ListView, View
from elaboradorapp.utils import GeraPDFMixin
from .models import Question, Disciplina, Conteudo
from django.db.models import Q

disciplina = ''
conteudo = ''
serie = ''
dificuldade = ''

def att_values(disc, cont, ser, dific):
    global disciplina
    global conteudo 
    global serie
    global dificuldade
    disciplina = disc
    conteudo = cont
    serie = ser
    dificuldade = dific




class ElaboradorApp(ListView):
    model = Question
    template_name = 'elaboradorapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(ElaboradorApp, self).get_context_data(**kwargs)
        context['disciplinas'] = Disciplina.objects.all()
        context['conteudos'] = Conteudo.objects.all()
        
        disciplina = self.request.GET.get('disciplina_value')
        conteudo = self.request.GET.get('conteudo_value')
        serie = self.request.GET.get('serie_value')
        dificuldade = self.request.GET.get('dificuldade_value')

        att_values(disciplina, conteudo, serie, dificuldade)
        return context

class ListarQuestoes(ListView):
    model = Question
    template_name = 'elaboradorapp/listar_questoes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questoes = Question.objects.all()

        # if disciplina:
        #     questoes = str(Question.objects.filter(disciplina='fisica'))
        #     print(questoes)
            
        
        context.update({
            'questoes': questoes,
        })
        return context


class ListarQuestoesPDF(View, GeraPDFMixin):
    def get(self, request, *args, **kwargs):
        questao = Question.objects.all()
        dados = {
            'questoes': questao
        }
        pdf = GeraPDFMixin()
        return pdf.render_to_pdf('elaboradorapp/listar_questoes.html', dados)
