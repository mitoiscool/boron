reveal = (element) => {
    obj = document.querySelector(element)
    if (obj.classList.contains("hidden")) {
        obj.classList.remove("hidden")
    } else {
        obj.classList.add("hidden")
    }
}

toclipboard = (element) => {
    var text = document.querySelector(element)
    navigator.clipboard.writeText(text.textContent)
    alert("Copied to clipboard")
}
