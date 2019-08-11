// $(function () { $('#collapseOne').collapse('hide')});

window.onload = function () {
    $(function () {
        var picker1 = $('#userselectWorkDatetime').datetimepicker({
            format: 'YYYY-MM-DD',
            locale: moment.locale('zh-cn'),
        });
        picker1.on('dp.change', function (e) {
            var date1 = $('#userselectWorkDatetime input').val()
            //query_date: date1
            var query_data = {
                query_date: date1
            }
            $.ajax({
                url: '/api/getWorkConclusion/',
                type: 'POST',
                data: query_data,
                success: function (data) {
                    var data_obj = JSON.parse(data)
                    if (data_obj.length != 0) {
                        $('#myModal textarea').val(data_obj[0]['conclusion'])
                        $('.top-left>h3>span').text('已提交')
                    } else {
                        $('#myModal textarea').val('')
                        $('.top-left>h3>span').text('未提交')
                    }
                },
            })

            $.ajax({
                url: '/api/getWorkList/',
                type: 'POST',
                data: query_data,
                success: function (data) {
                    var data_obj = JSON.parse(data)
                    $('#mytab').bootstrapTable('load', data_obj)
                    var finished = 0
                    for (let i in data_obj) {
                        if (data_obj[i]['state'] == '已提交')
                            finished++
                    }
                    $('.finished').text(finished.toString())
                    $('.unfinished').text((data_obj.length - finished).toString())

                },
            })
        })
        $('#Acceptance_time_div,#reply_time_div,#send_power_time_div,#design_send_time_div,#design_complete_time_div,#construction_send_time_div,#construction_complete_time_div,#release_time_div').datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            locale: moment.locale('zh-cn'),
        });

        $(".modal").draggable({
            handle: ".modal-header",  // 只能点击头部拖动
            cursor: 'move',
            refreshPositions: false,
        });
    });

    $.ajax({
        url: '/api/getWorkConclusion/',
        type: 'POST',
        success: function (data) {
            var data_obj = JSON.parse(data)
            if (data_obj.length != 0) {
                $('#myModal textarea').val(data_obj[0]['conclusion'])
                $('.top-left>h3>span').text('已提交')
            }
        },
    })


    $('#mytab').bootstrapTable({
        method: 'POST',
        // url: "/api/getWorkList/",//请求路径
        striped: true, //是否显示行间隔色
        pageNumber: 1, //初始化加载第一页
        pagination: true,//是否分页
        sidePagination: 'client',//server:服务器端分页|client：前端分页
        pageSize: 10,//单页记录数
        pageList: [5, 10, 20, 30],//可选择单页记录数
        // showRefresh: true,//刷新按钮
        columns: [
            {
                title: '任务id',
                field: 'id',
                sortable: true
            },
            {
                title: '户号',
                field: 'user_no',
                sortable: true
            }, {
                title: '户名',
                field: 'user_na',
                sortable: true
            }, {
                title: '业务类型',
                field: 'business_type',
            }, {
                title: '流程号',
                field: 'process_no',
            }, {
                title: '容量',
                field: 'capacity',
            }, {
                title: '地址',
                field: 'address',
            }, {
                title: '详情',
                field: '',
                formatter: operation
            },
        ],
    });

    function operation(value, row, index) {
        var htm = null
        if (row['state'] == '已提交') {
            htm = '<button class="btn btn-primary btn-sm" onclick="detailed_pop_init(' + index + ')" data-toggle="modal" data-target="#detailed_pop">\n' +
                '                                        已完成\n' +
                '                                    </button>'
        } else if (row['state'] == '已保存') {
            htm = '<button class="btn btn-info btn-sm" onclick="detailed_pop_init(' + index + ')" data-toggle="modal" data-target="#detailed_pop">\n' +
                '                                        已保存\n' +
                '                                    </button>'
        } else {
            htm = '<button class="btn btn-success btn-sm" onclick="detailed_pop_init(' + index + ')" data-toggle="modal" data-target="#detailed_pop">\n' +
                '                                        未提交\n' +
                '   </button>'
        }
        return htm
    }


    $.ajax({
        url: "/api/getWorkList/",//请求路径
        type: 'POST',
        success: function (data) {
            var data_obj = JSON.parse(data)
            $('#mytab').bootstrapTable('load', data_obj)
            var finished = 0
            for (let i in data_obj) {
                if (data_obj[i]['state'] == '已提交')
                    finished++
            }
            $('.finished').text(finished.toString())
            $('.unfinished').text((data_obj.length - finished).toString())

        },
    })


    $("td,th").addClass("text-center");
}

let detailed_pop_init = function (index) {
    var row = $('#mytab').bootstrapTable('getData')[index]
    for (let i in row) {
        if (row[i] != 'None')
            $('#detailed_pop_form textarea[name="' + i + '"],input[name="' + i + '"]').val(row[i])
    }

}

let save_submit = function () {
    $('#detailed_pop_form input[name="state"]').val('已保存')
    $('#detailed_pop_form').submit()
}

let work_submit = function () {
    $('#detailed_pop_form input[name="state"]').val('已提交')
    $('#detailed_pop_form').submit()
}