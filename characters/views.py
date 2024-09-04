import random

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from characters.models import Character
from characters.serializers import CharacterSerializer


@extend_schema(
    responses={status.HTTP_200_OK: CharacterSerializer}
)
@api_view(["GET"])
def get_random_character_view(request: Request) -> Response:
    """Get random character from Rick & Morty world"""
    character_ids = Character.objects.values_list("id", flat=True)
    random_id = random.choice(character_ids)
    random_character = Character.objects.get(id=random_id)
    serializer = CharacterSerializer(random_character)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterListView(generics.ListAPIView):
    serializer_class = CharacterSerializer

    def get_queryset(self):
        queryset = Character.objects.all()
        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter by name insensitive contains",
                required=False,
                type=str,
            ),
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:
        """List characters with filter by name"""
        return super().get(request, *args, **kwargs)
