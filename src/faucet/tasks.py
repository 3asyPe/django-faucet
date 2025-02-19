from celery import shared_task
from web3 import Web3
from .models import TransactionLog
from django.conf import settings
from django.db import transaction


@shared_task
def check_pending_transactions():
    web3 = Web3(Web3.HTTPProvider(settings.RPC))
    pending_txs = TransactionLog.objects.filter(success__isnull=True)
    updates = []
    for tx in pending_txs:
        try:
            receipt = web3.eth.get_transaction_receipt(tx.tx_id)
            if receipt is not None:
                tx.success = (receipt.status == 1)
                updates.append(tx)
        except Exception:
            continue

    with transaction.atomic():
        for tx in updates:
            tx.save(update_fields=['success'])

