from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


class GetUser(APIView):
    def get(self, *args, **kwargs):
        # return Response(
        #     data={
        #         "avatar": "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp",
        #         "title": "Marat Sharshenaliev",
        #         "instagram_account": "sadaqa.kg",
        #         "supporting_count": "1923 сом",
        #         "supporting_at": "19 дней",
        #         "tranzaction_count": "3",
        #         "isActive": True
        #     }
        # )

        return Response(data={})
