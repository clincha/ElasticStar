import os
import time

from datetime import datetime
from dotenv import load_dotenv

from starling import Starling

if __name__ == '__main__':
    load_dotenv()

    starling = Starling(
        os.getenv("STARLING_ACCESS_TOKEN"),
        sandbox=False
    )
    main_account = starling.get_accounts()[0]['accountUid']
    main_category = starling.get_accounts()[0]['defaultCategory']

    start_date = datetime(2023, 4, 6)
    end_date = datetime(2024, 4, 5, 23, 59, 59)

    transactions = starling.get_transaction_feed(main_account, start_date, end_date)

    for transaction in transactions:
        time.sleep(1)  # Sleep for a second to avoid rate limiting
        if transaction['hasAttachment']:
            attachments = starling.get_transaction_attachments(main_account, main_category, transaction['feedItemUid'])
            starling.download_transaction_attachment(main_account,
                                                     main_category,
                                                     transaction['feedItemUid'],
                                                     attachments[0]['feedItemAttachmentUid'],
                                                     attachments[0]['attachmentType']
                                                     )
