from rest_framework import serializers
from .models import CriteriosProva, Questao, Gabarito, NivelDificuldade, TipoQuestao

class QuestaoSerializer(serializers.ModelSerializer):
    tipo = serializers.ChoiceField(choices=TipoQuestao.choices)
    nivel_dificuldade = serializers.ChoiceField(choices=NivelDificuldade.choices, required=False)
    opcoes = serializers.JSONField(required=False)

    class Meta:
        model = Questao
        fields = '__all__'

class CriteriosProvaSerializer(serializers.ModelSerializer):
    #Para exibir texto, ao invés de chave estrangeira
    tipos_questoes = serializers.CharField()
    dificuldade = serializers.CharField()
    questoes = QuestaoSerializer(many=True, read_only=True)  # Serializa as questões relacionadas

    class Meta:
        model = CriteriosProva
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tipos_questoes'] = instance.get_tipos_questoes_display()
        representation['dificuldade'] = instance.get_dificuldade_display()
        return representation

class GabaritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gabarito
        fields = '__all__'