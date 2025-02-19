
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app.utils import get_client_ip
from .serializers import FundRequestSerializer
from faucet.faucet_toolkit import FaucetToolkit


logger = logging.getLogger(__name__)


@api_view(['POST'])
def fund_api(request):
    """
    API endpoint to process fund requests.
    """
    serializer = FundRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    dest_wallet = serializer.validated_data['wallet_address']
    source_ip = get_client_ip(request)
    faucet_toolkit = FaucetToolkit()

    logger.info(f'Processing fund request for {dest_wallet} from {source_ip}')

    tx_id = faucet_toolkit.process_fund(dest_wallet, source_ip)
    return Response({'transaction_id': tx_id}, status=status.HTTP_200_OK)

@api_view(['GET'])
def stats_api(_):
    """
    API endpoint to get statistics of transactions in the last 24 hours.
    """
    faucet_toolkit = FaucetToolkit()
    stats_dict = faucet_toolkit.get_stats()
    return Response(stats_dict, status=status.HTTP_200_OK)
