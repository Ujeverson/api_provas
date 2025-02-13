from django.db import models
from django.utils.translation import gettext_lazy as _

class NivelDificuldade(models.TextChoices):
    LEMBRAR = 'lembrar', _('Lembrar')
    ENTENDER = 'entender', _('Entender')
    APLICAR = 'aplicar', _('Aplicar')
    ANALISAR = 'analisar', _('Analisar')
    AVALIAR = 'avaliar', _('Avaliar')
    CRIAR = 'criar', _('Criar')

class TipoQuestao(models.TextChoices):
    MULTIPLA_ESCOLHA = 'multipla_escolha', _('Múltipla Escolha')
    DISSERTATIVA = 'dissertativa', _('Dissertativa')
    VERDADEIRO_FALSO = 'verdadeiro_falso', _('Verdadeiro/Falso')


class CriteriosProva(models.Model):
    tema = models.CharField(max_length=200)
    dificuldade = models.CharField(
        max_length=20,
        choices=NivelDificuldade.choices,
        default=NivelDificuldade.LEMBRAR
    )
    quantidade_questoes = models.PositiveIntegerField()
    tipos_questoes = models.CharField(
        max_length=100,
        choices=TipoQuestao.choices,
        # Permite múltiplos tipos, separados por vírgula
    )
    curriculo = models.TextField(blank=True, null=True)  # Opcional

    def __str__(self):
        return f"Prova sobre {self.tema} ({self.get_dificuldade_display()})"

class Questao(models.Model):
    prova = models.ForeignKey(
        CriteriosProva,
        on_delete=models.CASCADE,  # Se a prova for excluída, as questões também são
        related_name='questoes'  # Acesso reverso: prova.questoes
    )
    tipo = models.CharField(
        max_length=20,
        choices=TipoQuestao.choices
        )
    enunciado = models.TextField()
    opcoes = models.JSONField(blank=True, null=True)  # Para múltipla escolha
    resposta = models.TextField() #Resposta pode ser dissertativa, V ou F, ou a letra da múltipla escolha
    nivel_dificuldade = models.CharField(
        max_length=20,
        choices=NivelDificuldade.choices,
        default=NivelDificuldade.LEMBRAR,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.enunciado


class Gabarito(models.Model):
    prova = models.OneToOneField(
        CriteriosProva,
        on_delete=models.CASCADE,  # Se a prova for excluída, o gabarito também é
        related_name='gabarito'  # Acesso reverso: prova.gabarito
    )
    respostas = models.JSONField()

    def __str__(self):
        return f"Gabarito da prova {self.prova.id}"