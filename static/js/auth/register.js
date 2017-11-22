$('.gender').dropdown({
    onChange: function(value, text, $selectedItem) {
        $('#gender').val(value);
    }
});

////////////////////////////提交注册表单
$('#register').click(function () {
    var data = {};
    var registerForm = $('#register-form');
    var url = '/register';
    var d = registerForm.serializeArray();
    $.each(d, function() {
        data[this.name] = this.value;
    });
    $.ajax({
        async : false,
        url: url,
        type: "post",
        data: data,
        dataType: "json",
        success: function (ret) {
            if(ret.success){
                showMessage('success', '注册成功,稍后自动跳转登录界面...', 2000);
                setTimeout(function () {
                    hrefUrl('/login');
                }, 3000);
            } else {
                showMessage('error', ret.error);
            }
        },
        error: function (ret) {
            console.log(ret);
            showMessage('error', '服务器开小差');
        }
    });
});
