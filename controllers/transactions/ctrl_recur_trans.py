



class RecurringTransactionController:
    def get_all_recurring_transactions() -> TransactionResponse:
        r_trans = RecurringTransaction.query.order_by(
            RecurringTransaction.expected_day.asc()).all()
        return TransactionResponse(
            response_code=200,
            message=f"Retrieved {len(r_trans)} recurring transactions.",
            transactions=[TransactionInterface(
                r_tran, r_tran.category, r_tran.account) for r_tran in r_trans]
        )


    def get_rtran_by_id(rtranid: int) -> TransactionResponse:
        r_tran = RecurringTransaction.query.filter(
            RecurringTransaction.rtranid == rtranid).one_or_none()

        if r_tran is None:
            return TransactionResponse(
                response_code=404,
                message="No transactions found",
                transactions=[None]  # type: ignore
            )

        return TransactionResponse(
            response_code=200,
            message=f"Successfully retrieved transaction {rtranid}.",
            transactions=[TransactionInterface(
                r_tran, r_tran.category, r_tran.account)]
        )


    def insert_recurring_transaction(transaction_data: dict) -> TransactionResponse:
        # Make sure credit values are negative
        if transaction_data.get('transaction_type', '') == 'credit':
            if transaction_data.get('amount', 0) > 0:
                transaction_data['amount'] = transaction_data['amount'] * -1

        # ToDo: Check for record with the exact same values?

        transaction: RecurringTransaction = RecurringTransaction(
            expected_day=transaction_data.get('expected_day'),
            merchant_name=transaction_data.get('merchant_name', ''),
            categoryid=transaction_data.get('category', 1),
            amount=transaction_data.get('amount', 0),
            accountid=transaction_data.get('account', 1),
            transaction_type=transaction_data.get('transaction_type'),
            is_monthly=transaction_data.get('is_monthly', True),
            note=transaction_data.get('note', ''),
        )

        db.session.add(transaction)
        db.session.commit()

        return TransactionResponse(
            response_code=200,
            message="Transaction insert successful.",
            transactions=[TransactionInterface(
                transaction, transaction.category, transaction.account)]
        )


    def update_recurring_transaction(transaction_data: dict) -> TransactionResponse:
        transaction: RecurringTransaction = RecurringTransaction.query.filter(
            RecurringTransaction.rtranid == transaction_data.get('rtranid')).one_or_none()

        if transaction is None:
            return TransactionResponse(
                response_code=404,
                message=f"Transaction { transaction_data.get('rtranid')} not found.",
                transactions=[None]  # type: ignore
            )

        # Make sure credit values are negative
        if transaction_data.get('transaction_type', '') == 'credit':
            if transaction_data.get('amount', 0) > 0:
                transaction_data['amount'] = transaction_data['amount'] * -1

        if transaction_data.get('expected_day') != transaction.expected_day:
            transaction.expected_day = transaction_data.get(
                'expected_day', '')  # type: ignore
        if transaction_data.get('merchant_name') != transaction.merchant_name:
            transaction.merchant_name = transaction_data.get(
                'merchant_name', '')  # type: ignore
        if transaction_data.get('category') != transaction.categoryid:
            transaction.categoryid = transaction_data.get(
                'category', 1)  # type: ignore
        if transaction_data.get('amount') != transaction.amount:
            transaction.amount = transaction_data.get('amount', 0)  # type: ignore
        if transaction_data.get('account') != transaction.accountid:
            transaction.accountid = transaction_data.get(
                'account', 0)  # type: ignore
        if transaction_data.get('transaction_type') != transaction.transaction_type:
            transaction.transaction_type = transaction_data.get(
                'transaction_type', '')  # type: ignore
        if transaction_data.get('is_monthly') != transaction.is_monthly:
            transaction.is_monthly = transaction_data.get(
                'is_monthly', True)  # type: ignore
        if transaction_data.get('note') != transaction.note:
            transaction.note = transaction_data.get('note', '')  # type: ignore

        db.session.commit()

        return TransactionResponse(
            response_code=200,
            message="Transaction update successful.",
            transactions=[TransactionInterface(
                transaction, transaction.category, transaction.account)]
        )


    def delete_recurring_transaction(rtranid: int) -> TransactionResponse:
        transaction: RecurringTransaction = RecurringTransaction.query.filter(
            RecurringTransaction.rtranid == rtranid).one_or_none()

        if transaction is None:
            raise ValueError(f"{rtranid} is not a valid transaction id.")

        transactions = [TransactionInterface(
            transaction, transaction.category, transaction.account)]

        db.session.delete(transaction)
        db.session.commit()

        return TransactionResponse(
            response_code=200,
            message=f"Transaction {rtranid} deleted successfully.",
            transactions=transactions
        )


    def apply_recurring_transactions(rtrans_data: dict[str, str]) -> TransactionResponse:
        transactions = []
        for rtranid in rtrans_data.get("RTranIDs", "").split(","):
            # ToDo: Check Response
            get_rtran_response = get_rtran_by_id(int(rtranid))
            rtran = get_rtran_response.transactions[0]

            rtran_year = rtrans_data.get('rtran_year')
            rtran_month = rtrans_data.get('rtran_month')

            if rtran_year is None or rtran_month is None:
                return TransactionResponse(
                    response_code=400,
                    message="Bad Request: Please submit a year and month for correct processing.",
                    transactions=[]
                )

            tran_data = {
                # type: ignore
                "transaction_date": date(year=int(rtran_year), month=int(rtran_month), day=rtran.transaction.expected_day),
                # type: ignore
                "cashflow_date": date(year=int(rtran_year), month=int(rtran_month), day=rtran.transaction.expected_day),
                "merchant_name": rtran.transaction.merchant_name,  # type: ignore
                "category": rtran.transaction.categoryid,  # type: ignore
                "amount": rtran.transaction.amount,  # type: ignore
                "account": rtran.transaction.accountid,  # type: ignore
                "transaction_type": rtran.transaction.transaction_type,  # type: ignore
                "note": rtran.transaction.note,  # type: ignore
            }
            # ToDo: Check Response
            tran_insert_response = insert_transaction(transaction_data=tran_data)
            transactions.append(tran_insert_response.transactions[0])

        return TransactionResponse(
            response_code=200,
            message=f"Successfully inserted {len(transactions)} recurring transactions.",
            transactions=transactions
        )