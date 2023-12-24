function init() {
    init_events()
    init_filter_session()
}

function toggle_account_rows(event) {
    let account = event.target.id.replace('-filter','')
    let account_rows = document.querySelectorAll(`[account="${account}"]`)
    if (event.target.checked) {
        sessionStorage.setItem(event.target.id, true)
        account_rows.forEach((row) => {
            row.classList.remove("hidden")
        })
    } else {
        sessionStorage.setItem(event.target.id, false)
        account_rows.forEach((row) => {
            row.classList.add("hidden")
        })
    }
}

function clear_account_filters() {
    let account_filter_array = document.querySelectorAll(".account-filter")
    
    account_filter_array.forEach((filter) => {
        if (filter.checked === false) {
            filter.click()
        }
    })
}

function init_events() {
    document.getElementById("transaction_type").addEventListener("blur", (event) => {
        let merchant_name = document.getElementById("merchant_name")
        let transfer_account = document.getElementById("transfer_account")
        if (['trfr', 'ccp', 'finpay'].includes(event.target.value)) {
            // DECISION: hide or disable category selector?
            merchant_name.classList.add("hidden")
            merchant_name.labels[0].classList.add("hidden")
            merchant_name.value = 'Transfer'

            transfer_account.classList.remove("hidden")
            transfer_account.labels[0].classList.remove("hidden")
            transfer_account.focus()


        } 
        else {
            transfer_account.classList.add("hidden")
            transfer_account.labels[0].classList.add("hidden")

            merchant_name.classList.remove("hidden")
            merchant_name.labels[0].classList.remove("hidden")
            merchant_name.value = ''
        }
    })

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
}

function init_filter_session() {
    const filterArray = document.querySelectorAll(".account-filter")
    filterArray.forEach((filter) => {
        let filter_id = filter.id;
        filter_state = sessionStorage.getItem(filter_id)
        if (filter_state === null) {
            sessionStorage.setItem(filter_id, true)
            document.getElementById(filter_id).checked = true;
        } else {
            document.getElementById(filter_id).checked = (filter_state === 'true')
        }
    })
}

init();