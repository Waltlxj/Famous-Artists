window.onload = function () {
    window.currentlink = window.location.href;
    arr = currentlink.split('/')
    page = arr[arr.length - 1].split('.')[0];
    console.log(page)
    if (page == "index") {
        document.getElementById("index").style.borderBottom = ("solid")
    }
    if (page == "data") {
        document.getElementById("data").style.borderBottom = ("solid")
    }
}
changehi = function (element) {
    window.alert(element)
}