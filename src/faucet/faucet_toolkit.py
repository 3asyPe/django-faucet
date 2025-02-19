from datetime import timedelta
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from eth_account.signers.local import LocalAccount
from web3 import Web3

from app.exceptions import RateLimitException
from .models import TransactionLog


class FaucetToolkit:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(settings.RPC))
        self.eth_account: LocalAccount = self.web3.eth.account.from_key(settings.FAUCET_PRIVATE_KEY)

    @transaction.atomic
    def process_fund(self, dest_wallet: str, source_ip: str) -> str:
        now = timezone.now()
        cutoff = now - timedelta(seconds=settings.TIMEOUT_SECONDS)
        if TransactionLog.objects.filter(
            timestamp__gte=cutoff
        ).filter(
            Q(source_ip=source_ip) | Q(wallet_address=dest_wallet)
        ).exists():
            raise RateLimitException()

        try:
            # Prepare the transaction.
            tx_id = self._send_funds(dest_wallet)

            # Log the successful transaction.
            TransactionLog.objects.create(
                wallet_address=dest_wallet,
                source_ip=source_ip,
                tx_id=tx_id
            )
            return tx_id

        except Exception as e:
            # Log the failure.
            TransactionLog.objects.create(
                wallet_address=dest_wallet,
                source_ip=source_ip,
                success=False
            )
            raise e

    def _send_funds(self, dest_wallet: str) -> str:
        nonce = self.web3.eth.get_transaction_count(self.eth_account.address, 'pending')
        base_tx = {
            'nonce': nonce,
            'to': dest_wallet,
            'value': self.web3.to_wei(settings.AMOUNT_ETH, 'ether'),
            'gasPrice': self.web3.eth.gas_price,
        }
        estimated_gas = self.web3.eth.estimate_gas({**base_tx, 'from': self.eth_account.address})
        base_tx['gas'] = estimated_gas

        signed_tx = self.eth_account.sign_transaction(base_tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash.hex()
    
    def get_stats(self) -> dict:
        now = timezone.now()
        cutoff = now - timedelta(hours=24)
        success_count = TransactionLog.objects.filter(timestamp__gte=cutoff, success=True).count()
        failure_count = TransactionLog.objects.filter(timestamp__gte=cutoff, success=False).count()
        return {
            'successful_transactions': success_count,
            'failed_transactions': failure_count
        }