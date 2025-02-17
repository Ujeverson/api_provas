from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CriteriosProva, Questao, Gabarito, NivelDificuldade, TipoQuestao
from .serializers import CriteriosProvaSerializer
from unittest.mock import patch
from django.contrib.auth.models import User  # Importe o modelo User


# --- Testes Unitários ---

class NivelDificuldadeTestCase(TestCase):
    def test_niveis_dificuldade(self):
        self.assertEqual(NivelDificuldade.LEMBRAR, 'lembrar')
        self.assertEqual(NivelDificuldade.ENTENDER, 'entender')
        self.assertEqual(NivelDificuldade.APLICAR, 'aplicar')
        self.assertEqual(NivelDificuldade.ANALISAR, 'analisar')
        self.assertEqual(NivelDificuldade.AVALIAR, 'avaliar')
        self.assertEqual(NivelDificuldade.CRIAR, 'criar')

class TipoQuestaoTestCase(TestCase):
    def test_tipos_questao(self):
        self.assertEqual(TipoQuestao.MULTIPLA_ESCOLHA, 'multipla_escolha')
        self.assertEqual(TipoQuestao.DISSERTATIVA, 'dissertativa')
        self.assertEqual(TipoQuestao.VERDADEIRO_FALSO, 'verdadeiro_falso')

# --- Testes de Integração ---
class GerarProvaAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('gerar-prova')
        self.dados_validos = {
            'tema': 'Teste',
            'dificuldade': NivelDificuldade.LEMBRAR,
            'quantidade_questoes': 2,
            'tipos_questoes': f'{TipoQuestao.MULTIPLA_ESCOLHA},{TipoQuestao.DISSERTATIVA}',
            'curriculo': 'Teste de currículo'
        }
        self.dados_invalidos = {
            'tema': '',
            'dificuldade': 'invalido',
            'quantidade_questoes': -1,
            'tipos_questoes': 'tipo_invalido',
        }
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    @patch('provas.views.client.chat.completions.create')
    def test_criar_prova_com_sucesso(self, mock_groq_create):
        mock_groq_create.return_value.choices[0].message.content = """
        {
            "questoes": [
                {
                    "tipo": "multipla_escolha",
                    "enunciado": "Qual a capital do Brasil?",
                    "opcoes": ["A", "B", "C", "D"],
                    "resposta": "B",
                    "nivel_dificuldade": "lembrar"
                },
                {
                    "tipo": "dissertativa",
                    "enunciado": "Explique o que é fotossíntese.",
                    "resposta": "Fotossíntese é...",
                    "nivel_dificuldade": "entender"
                }
            ]
        }
        """
        response = self.client.post(self.url, self.dados_validos, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CriteriosProva.objects.count(), 1)
        self.assertEqual(Questao.objects.count(), 2)
        self.assertEqual(Gabarito.objects.count(), 1)

    def test_criar_prova_com_dados_invalidos(self):
        response = self.client.post(self.url, self.dados_invalidos, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detalhar_prova(self):
          #Criar uma prova
          response = self.client.post(self.url, self.dados_validos, format='json')
          #Pegar a prova
          url = reverse('detalhar-prova', kwargs={'id': response.data['id']})
          response = self.client.get(url)
          self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detalhar_gabarito(self):
        #Criar uma prova
        response = self.client.post(self.url, self.dados_validos, format='json')
        #Pegar o gabarito
        url = reverse('detalhar-gabarito', kwargs={'prova__id': response.data['id']})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BuscaQuestoes(TestCase): #Classe para testar os serviços, separadamente
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    @patch('provas.views.client.chat.completions.create')
    def test_criar_multipla_escolha(self, mock_groq):
        mock_groq.return_value.choices[0].message.content = """
        {
        "questoes": [
            {
            "tipo": "multipla_escolha",
            "enunciado": "Enunciado",
            "opcoes": ["A", "B", "C", "D"],
            "resposta": "B",
            "nivel_dificuldade": "lembrar"
            }
        ]
        }
        """

        #Dados de entrada
        dados_entrada = {
        'tema': 'Teste',
        'dificuldade': NivelDificuldade.LEMBRAR,
        'quantidade_questoes': 1,
        'tipos_questoes': TipoQuestao.MULTIPLA_ESCOLHA,
        'curriculo': 'Teste de currículo'
        }
        # Cria uma instância de CriteriosProva
        criterios = CriteriosProva.objects.create(**dados_entrada)
        #Chama o endpoint
        url = reverse('gerar-prova')
        response = self.client.post(url, dados_entrada, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    @patch('provas.views.client.chat.completions.create')
    def test_criar_dissertativa(self, mock_groq):
        mock_groq.return_value.choices[0].message.content = """
        {
        "questoes": [
            {
            "tipo": "dissertativa",
            "enunciado": "Enunciado",
            "resposta": "Resposta",
            "nivel_dificuldade": "lembrar"
            }
        ]
        }
        """
        #Dados de entrada
        dados_entrada = {
        'tema': 'Teste',
        'dificuldade': NivelDificuldade.LEMBRAR,
        'quantidade_questoes': 1,
        'tipos_questoes': TipoQuestao.DISSERTATIVA,
        'curriculo': 'Teste de currículo'
        }
        # Cria uma instância de CriteriosProva
        criterios = CriteriosProva.objects.create(**dados_entrada)
        #Chama o endpoint
        url = reverse('gerar-prova')
        response = self.client.post(url, dados_entrada, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('provas.views.client.chat.completions.create')
    def test_criar_verdadeiro_falso(self, mock_groq):
        mock_groq.return_value.choices[0].message.content = """
        {
        "questoes": [
            {
            "tipo": "verdadeiro_falso",
            "enunciado": "Enunciado",
            "resposta": "V",
            "nivel_dificuldade": "lembrar"
            }
        ]
        }
        """
        #Dados de entrada
        dados_entrada = {
        'tema': 'Teste',
        'dificuldade': NivelDificuldade.LEMBRAR,
        'quantidade_questoes': 1,
        'tipos_questoes': TipoQuestao.VERDADEIRO_FALSO,
        'curriculo': 'Teste de currículo'
        }
        # Cria uma instância de CriteriosProva
        criterios = CriteriosProva.objects.create(**dados_entrada)
        #Chama o endpoint
        url = reverse('gerar-prova')
        response = self.client.post(url, dados_entrada, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)