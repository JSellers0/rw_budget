document.getElementById("transaction_type").addEventListener("blur", (event) => {
    let merchant_name = document.getElementById("merchant_name")
    let transfer_account = document.getElementById("transfer_account")
    if (['trfr', 'ccp', 'finpay'].includes(event.target.value)) {
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

function toggle_account_rows(event) {
    let account = event.target.id.replace('-filter','')
    let account_rows = document.querySelectorAll(`[account="${account}"]`)
    account_rows.forEach((row) => {
        if (event.target.checked) 
            row.classList.remove("hidden")
        else row.classList.add("hidden")
    })
}

function clear_account_filters() {
    let account_filter_array = document.querySelectorAll(".account-filter")
    
    account_filter_array.forEach((filter) => {
        if (filter.checked === false) {
            filter.click()
        }
    })
}

// Add account filter click events
document.getElementById("pnc-spend-filter").addEventListener("click", toggle_account_rows)
document.getElementById("pnc-rewards-filter").addEventListener("click", toggle_account_rows)
document.getElementById("venture-filter").addEventListener("click", toggle_account_rows)
document.getElementById("quicksilver-filter").addEventListener("click", toggle_account_rows)
document.getElementById("cap-bills-filter").addEventListener("click", toggle_account_rows)
document.getElementById("pnc-bills-filter").addEventListener("click", toggle_account_rows)

document.getElementById("clear-account-filters").addEventListener("click", clear_account_filters)

// Filter Accordion
const choiceArray = document.querySelectorAll(".choice")

choiceArray.forEach((card) => {
    card.addEventListener("click", (event) => {
        if (event.target.id.includes("filter")) {
            choiceArray.forEach((element) => {
                element.classList.remove("expand", "unset")
                element.classList.add('unset')
            })
            card.classList.remove("unset")
            card.classList.add('expand')
        }
    });
});