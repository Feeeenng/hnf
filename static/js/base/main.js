function hideMessage(obj) {
    var msgItem = $(obj).parent();
    msgItem.transition({
        animation : 'drop out',
        onComplete : function() {
            $(this).remove();
        }
    });
}

function showMessage(category, msg) {
    var content = '';
    if(category == 'error') {
        content = '<div class="ui negative floating message" hidden><i class="close icon" onclick="hideMessage(this)"></i>' +
            '<div class="header"><i class="remove circle icon"></i>' + msg + '</div></div>';
    } else if(category == 'info') {
        content = '<div class="ui info floating message" hidden><i class="close icon" onclick="hideMessage(this)"></i>' +
            '<div class="header"><i class="info circle icon"></i>' + msg + '</div></div>';
    } else if(category == 'warning') {
        content = '<div class="ui warning floating message" hidden><i class="close icon" onclick="hideMessage(this)"></i>' +
            '<div class="header"><i class="warning circle icon"></i>' + msg + '</div></div>';
    } else if(category == 'success') {
        content = '<div class="ui positive floating message" hidden><i class="close icon" onclick="hideMessage(this)"></i>' +
            '<div class="header"><i class="check circle icon"></i>' + msg + '</div></div>';
    } else {
        content = '';
    }

    var last = $('#hnf-msg').prepend(content).children('div:first');
    last.transition({
        animation : 'drop in',
        onComplete : function() {
            setTimeout(function () {
                last.transition({
                    animation: 'fade out',
                    duration: '1s',
                    onComplete: function () {
                        last.remove();
                    }
                });
            }, 3000);
        }
    })
}