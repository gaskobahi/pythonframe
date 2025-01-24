from rest_framework.views import APIView
from rest_framework.response import Response
from base.abilities import define_abilities_for
from common.authentification.CustomIsAuthenticated import CustomIsAuthenticated

class AbilityRulesView(APIView):
    """
    API pour exposer les règles CASL pour l'utilisateur actuel.
    """
    permission_classes = [CustomIsAuthenticated]

    def get(self, request):
        rules = define_abilities_for(request.authUser.get('user'))
        return Response(rules)