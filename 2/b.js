var xhr = new XMLHttpRequest()

xhr.open("GET", "../first/laba.xml", true)
xhr.send()
const nodes = xhr.responseXML.querySelectorAll("laba")

function load(){
    console.log("gogo")
    var count = document.getElementById("input").value
    var converted = parseInt(count)
    var abs = converted
    if (converted < 0){
        abs = converted * - 1
    }

    const nodes = xhr.responseXML.querySelectorAll("laba")
    const total = nodes.length

    if (isNaN(converted)){
        alert("уровень должен быть числом")
        return
    }
    if (converted > total){
        alert("слишком много...")
    }

    var node = nodes[abs].textContent.split(" ")
    var toRev = node.slice(1)
    if (converted < 0){
        toRev.reverse()
    }
    var res = node[0] + toRev.join(" ")

    var elem = document.getElementById("123")
    elem.textContent = res
}


