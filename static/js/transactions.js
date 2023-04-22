document.getElementById("transaction_type").addEventListener("blur", (event) => {
    console.log("Blur MFer")
    if (['trfr', 'ccp'].includes(event.target.value)) {
        document.getElementById("merchant-data-list").classList.remove("hidden")
    } 
    else {
        document.getElementById("merchant-data-list").classList.add("hidden")
    }
    
})