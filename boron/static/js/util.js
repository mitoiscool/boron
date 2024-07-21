reveal = (element) => {
    obj = document.querySelector(element)
    if (obj.classList.contains("hidden")) {
        obj.classList.remove("hidden")
    } else {
        obj.classList.add("hidden")
    }
}