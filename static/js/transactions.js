document.getElementById("transaction_type").addEventListener("blur", (event) => {
    let merchant_name = document.getElementById("merchant_name")
    let transfer_account = document.getElementById("transfer_account")
    if (['trfr', 'ccp'].includes(event.target.value)) {
        // DECISION: hide or disable category selector?
        transfer_account.classList.remove("hidden")
        transfer_account.labels[0].classList.remove("hidden")

        merchant_name.classList.add("hidden")
        merchant_name.labels[0].classList.add("hidden")
        merchant_name.value = 'Transfer'
    } 
    else {
        transfer_account.classList.add("hidden")
        transfer_account.labels[0].classList.add("hidden")

        merchant_name.classList.remove("hidden")
        merchant_name.labels[0].classList.remove("hidden")
        merchant_name.value = ''
    }
})