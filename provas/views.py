from rest_framework import generics, status
from rest_framework.response import Response
from .models import CriteriosProva, Questao, Gabarito
from .serializers import CriteriosProvaSerializer, QuestaoSerializer, GabaritoSerializer
from groq import Groq  # Importe a biblioteca do Groq
import os
import json #Já importe aqui
from dotenv import load_dotenv

load_dotenv()

# Configure o cliente do Groq com a chave da API
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class GerarProvaView(generics.CreateAPIView):
    serializer_class = CriteriosProvaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        criterios = serializer.save()

        # --- Lógica para gerar questões com o Groq ---
        prompt = self.criar_prompt(criterios)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="mixtral-8x7b-32768",  # Modelo da LLM
            
        
        )

        # --- Processar a resposta do Groq ---
        questoes_geradas = self.processar_resposta_groq(chat_completion, criterios)

        # --- Criar as questões no banco de dados ---
        for questao_data in questoes_geradas:
            Questao.objects.create(prova=criterios, **questao_data)

        # --- Criar o gabarito ---
        respostas = {str(questao.id): questao.resposta for questao in criterios.questoes.all()}
        Gabarito.objects.create(prova=criterios, respostas=respostas)

        return Response(
            CriteriosProvaSerializer(criterios).data,
            status=status.HTTP_201_CREATED
        )

    def criar_prompt(self, criterios):
        # Constrói o prompt para o Groq
        prompt = f"""
        Gere {criterios.quantidade_questoes} questões sobre o tema '{criterios.tema}',
        com nível de dificuldade '{criterios.get_dificuldade_display()}'
        e com os seguintes tipos: {criterios.get_tipos_questoes_display()}.
        """
        if criterios.curriculo:
            prompt += f" Considere o seguinte currículo: {criterios.curriculo}."

        prompt += """
        Retorne as questões e respostas no seguinte formato JSON:
        {
          "questoes": [
            {
              "tipo": "multipla_escolha",
              "enunciado": "...",
              "opcoes": ["...", "..."],
              "resposta": "...",
              "nivel_dificuldade": "..."
            },
            {
              "tipo": "dissertativa",
              "enunciado": "...",
              "resposta": "...",
              "nivel_dificuldade": "..."
            }
          ]
        }
        """
        return prompt

    def processar_resposta_groq(self, chat_completion, criterios):
      # Extrai as questões e respostas do JSON retornado pelo Groq
        try:
            resposta_json = chat_completion.choices[0].message.content
            resposta = json.loads(resposta_json)
            questoes = resposta.get("questoes", [])

            # Valida e formata os dados das questões
            questoes_formatadas = []
            for questao in questoes:
                tipo = questao.get("tipo")
                enunciado = questao.get("enunciado")
                resposta_questao = questao.get("resposta")
                nivel = questao.get("nivel_dificuldade")
                opcoes = questao.get("opcoes", None)

                if not all([tipo, enunciado, resposta_questao]):
                    continue

                questao_formatada = {
                    "tipo": tipo,
                    "enunciado": enunciado,
                    "resposta": resposta_questao,
                    "nivel_dificuldade": nivel,
                    "opcoes": opcoes
                }
                questoes_formatadas.append(questao_formatada)
            return questoes_formatadas

        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Erro ao processar a resposta do Groq: {e}")
            return []
class DetalharProvaView(generics.RetrieveAPIView):
    queryset = CriteriosProva.objects.all()
    serializer_class = CriteriosProvaSerializer
    lookup_field = 'id'

class DetalharGabaritoView(generics.RetrieveAPIView):
    queryset = Gabarito.objects.all()
    serializer_class = GabaritoSerializer
    lookup_field = 'prova__id'