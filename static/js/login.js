window.onload = function () {
}

let register_submit = function () {
    var passwd = $('#register_new_form input[name="password"]:first').val()
    var repasswd = $('#register_new_form input[name="password"]:last').val()
    var name = $('#register_new_form input[name="name"]').val()
    var cell_phone_number = $('#register_new_form input[name="cell_phone_number"]').val()

    if (passwd != repasswd) {
        alert("两次输入的密码不一致")
    } else if (cell_phone_number == '' || name == '' || passwd == '' || repasswd == '') {
        alert('用户和电话号密码必填')
    } else {
        $('#register_new_form').submit()
    }

}


let modify_submit = function () {
    var passwd = $('#user_modify_form input[name="password"]:first').val()
    var repasswd = $('#user_modify_form input[name="password"]:last').val()
    var name = $('#user_modify_form input[name="name"]').val()
    var cell_phone_number = $('#user_modify_form input[name="cell_phone_number"]').val()
    if (passwd != repasswd) {
        alert("两次输入的密码不一致")
    } else if (cell_phone_number == '' || name == '' || passwd == '' || repasswd == '') {
        alert('用户和电话号密码必填')
    } else {
        $('#user_modify_form').submit()
    }

}