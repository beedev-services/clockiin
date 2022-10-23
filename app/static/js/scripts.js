console.log("JS file connected")

function auth() {
    var l = document.getElementById('login')
    var r = document.getElementById('reg')
    var t = document.getElementById('text')
    if (r.style.display === 'flex') {
        r.style.display = 'none'
        l.style.display = 'flex'
        l.style.flexDirection = 'column';
        t.innerHTML = 'Register'
    } else {
        l.style.display = 'none'
        r.style.display = 'flex'
        r.style.flexDirection = 'column';
        t.innerHTML = 'Login'
    }
}

function showField() {
    var selection = document.reg.role.value
    var regcode = document.getElementById('regcode')
    if(selection != 'employee') {
        if(regcode.style.display === 'flex') {
            regcode.style.display = 'flex'
            regcode.style.flexDirection = 'column'
        } else {
            regcode.style.display = 'flex'
            regcode.style.flexDirection = 'column'
        }
    } else {
        if(regcode.style.display === 'flex') {
            regcode.style.display = 'none'
        } else {
            regcode.style.display = 'none'
        }
    }
}
