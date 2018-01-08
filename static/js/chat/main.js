function newRoom() {
    var url = '/chat/new_room';
    var data = $('#new-room-form').serialize();
    var code = true;
    $.ajax({
        async : false,
        url: url,
        type: "POST",
        data: data,
        dataType   : "json",
        success: function(ret){
            if(!ret["success"]) {
                showMessage('error', ret['error'], 3000, 'create-room-msg');
                code = false;
            } else {
                // load数据列表
                var payload = {};
                reloadListData(payload);
            }
        },
        error: function (ret) {
            showMessage('error', '网络异常', 3000, 'create-room-msg');
            code = false;
        }
    });
    return code;
}

function clearForm() {
    $('#new-room-form')[0].reset();
}

function destorySelf() {
    $('#creator_tag').remove();
    var payload = $('#room-search-form').serialize();
    reloadListData(payload);
}

function reloadData() {}

function loadByCreatorId(obj) {
    var creator = $(obj).text();
    var creator_id = $(obj).data('creator_id');
    var content = '' +
        '<div class="fields" id="creator_tag">' +
            '<div class="field">' +
                '<div class="ui label">' +
                    '<i class="user icon"></i>' + creator +
                    '<i class="delete icon" onclick="destorySelf()"></i>' +
                    '<input type="hidden" name="creator_id" value="' + creator_id + '">' +
                '</div>' +
            '</div>' +
        '</div>';

    if($('#creator_tag').length > 0){
        $('#creator_tag').remove();
    }
    $('#room-search-form').append(content);

    var payload = $('#room-search-form').serialize();
    reloadListData(payload);
}

function reloadListData(data) {
    var url = '/chat/room_list';
    var code = true;
    $.ajax({
        async : false,
        url: url,
        type: "POST",
        data: data,
        dataType   : "json",
        success: function(ret){
            if(!ret["success"]) {
                showMessage('error', ret['error'], 3000);
                code = false;
            } else {
                // 列表数据展示
                var list_data = ret["data"];
                var total = ret["total"];
                var per_page = ret["per_page"];
                $("#tab-list").empty();
                $.each(list_data, function(index, val) {
                    $("#tab-list").append(
                        '<tr>' +
                            '<td class="left aligned"><strong>' + val["name"] + '</strong>(' + val["id"] + ')' + '</td>' +
                            '<td><a style="cursor: pointer" onclick="loadByCreatorId(this)" data-creator_id="' + val["creator_id"] + '">' + val["creator"] + '</a></td>' +
                            '<td>' + val["members"] + '</td>' +
                            '<td>' + val["created_at"] + '</td>' +
                            '<td>' +
                                '<div class="ui animated teal tiny button" tabindex="0">' +
                                    '<div class="visible content">加入</div>' +
                                    '<div class="hidden content">' +
                                        '<i class="add icon"></i>' +
                                    '</div>' +
                                '</div>' +
                            '</td>' +
                        '</tr>'
                    );
                } );
            }
        },
        error: function (ret) {
            showMessage('error', '网络异常', 3000);
            code = false;
        }
    });
    return code;
}

$('#room-search-btn').click(function () {
    var payload = $('#room-search-form').serialize();
    reloadListData(payload);

});

$('#new_room_box').modal({
    transition: 'vertical flip',
    onShow: reloadData,
    onApprove: newRoom,
    onDeny: clearForm,
    allowMultiple: false
}).modal('attach events', '#new_room_btn', 'show');

$(document).ready(function () {
    var payload = {};
    reloadListData(payload);
});