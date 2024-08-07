function init() {
    init_events()
    init_filter_session()
    let today = new Date()
    let today_value = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}` 
    document.getElementById('transaction_date').value = today_value
    document.getElementById('cashflow_date').value = today_value
}

function toggle_account_rows(event) {
    let account = event.target.id.replace('-filter','')
    const trans_accordion = document.getElementById("transaction-accordion")
    const account_rows = trans_accordion.querySelectorAll(`[account="${account}"]`)
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
    const account_filters = document.getElementById("account-filters")
    const filterArray = account_filters.querySelectorAll(".account-filter")
    
    filterArray.forEach((filter) => {
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
            merchant_name.focus()
        }
    })

    // Add account filter click events
    document.getElementById("pnc-spend-filter").addEventListener("click", toggle_account_rows)
    document.getElementById("pnc-rewards-filter").addEventListener("click", toggle_account_rows)
    document.getElementById("venture-filter").addEventListener("click", toggle_account_rows)
    document.getElementById("barclays-filter").addEventListener("click", toggle_account_rows)
    document.getElementById("quicksilver-filter").addEventListener("click", toggle_account_rows)
    document.getElementById("cap-bills-filter").addEventListener("click", toggle_account_rows)
    document.getElementById("pnc-bills-filter").addEventListener("click", toggle_account_rows)

    document.getElementById("clear-account-filters").addEventListener("click", clear_account_filters)

    // Filter Accordion
    const filter_panel = document.getElementById("transaction-filters")
    const choiceArray = filter_panel.querySelectorAll(".choice")

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

    document.getElementById("cashflow_date").addEventListener("focus", (event) => {
        event.target.value = document.getElementById('transaction_date').value
    })
}

function init_filter_session() {
    const account_filters = document.getElementById("account-filters")
    const filterArray = account_filters.querySelectorAll(".account-filter")
    filterArray.forEach((filter) => {
        let filter_id = filter.id;
        filter_state = sessionStorage.getItem(filter_id)
        if (filter_state === null) {
            console.log('init')
            sessionStorage.setItem(filter_id, document.getElementById(filter_id).checked)
        }
    })
}

function apply_filter_session_state(){
    console.log('apply filters')
    const account_filters = document.getElementById("account-filters")
    const filterArray = account_filters.querySelectorAll(".account-filter")
    filterArray.forEach((filter) => {
        let filter_id = filter.id;
        filter_state = sessionStorage.getItem(filter_id)
        if (filter_state === 'false') {
            document.getElementById(filter_id).click()
        }
    })
}

init();
document.onload = apply_filter_session_state();