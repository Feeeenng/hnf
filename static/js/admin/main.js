$('.admin-mgmt-dropdown').dropdown({on:'hover'});

///////////////////////////// 消息提示 start
function hideMessage(obj) {
    var msgItem = $(obj).parent();
    msgItem.transition({
        animation : 'drop out',
        onComplete : function() {
            $(this).remove();
        }
    });
}

function showMessage(category, msg, duration) {
    if(!duration){
        duration = 3000;  // ms
    }

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

    var hnfMsg = $('#hnf-msg');
    var size = hnfMsg.children().length;
    if(size < 5) {
        var first = hnfMsg.prepend(content).children('div:first');
        first.transition({
            animation: 'drop in',
            onComplete: function () {
                setTimeout(function () {
                    first.transition({
                        animation: 'fade out',
                        duration: '1s',
                        onComplete: function () {
                            if (first) {
                                first.remove();
                            }
                        }
                    });
                }, duration);
            }
        })
    }
}
/////////////////////////////消息提示 end

// 跳转url
function hrefUrl(url) {
    location.href = url;
}

// 倒计时跳转
function countDown(seconds, url, elm) {
    elm.html('(' + seconds + 's)');
    if(--seconds > 0) {
        setTimeout(function () {
            countDown(seconds, url, elm);
        }, 1000);
    } else {
        hrefUrl(url);
    }
}