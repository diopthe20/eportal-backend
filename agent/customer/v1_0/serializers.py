from rest_framework import serializers

from agent.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=["cv_extract", "table_extract", "id_extract"]
    )
    status = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = ["id", "type", "created_at", "status", "count"]

    def get_status(self, instance: Agent):
        all = instance.pdf_agent
        total = all.count()
        completed = all.filter(status=2).count()
        return int(completed / total * 100)

    def get_count(self, instance: Agent):
        all = instance.pdf_agent
        return all.count()


class UploadPdfSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=["cv_extract", "table_extract", "id_extract"]
    )


class RetrieveAgentSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=["cv_extract", "table_extract", "id_extract"]
    )
    status = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = ["id", "type", "created_at", "status", "count"]

    def get_count(self, instance: Agent):
        all = instance.pdf_agent
        return all.count()

    def get_status(self, instance: Agent):
        all = instance.pdf_agent
        total = all.count()
        completed = all.filter(status=2).count()
        return int(completed / total * 100)
