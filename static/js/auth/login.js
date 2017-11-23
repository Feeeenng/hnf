$('.remember').checkbox();

$('#register-href').click(function () {
    hrefUrl('/register');
});

////////////////////////////提交注册表单
$('#login').click(function () {
    var data = {};
    var loginForm = $('#login-form');
    var url = loginForm.attr('action');
    var d = loginForm.serializeArray();
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
                hrefUrl(ret.url);
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

$(function(){
    document.onkeydown = function(e){
        var ev = document.all ? window.event : e;
        if(ev.keyCode==13) {
            $('#login').click();
        }
    }
});