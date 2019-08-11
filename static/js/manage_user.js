// $(function () { $('#collapseOne').collapse('hide')});

window.onload = function () {
    $(".modal").draggable({
        handle: ".modal-header",  // 只能点击头部拖动
        cursor: 'move',
        refreshPositions: false,
    });

    $(function () {
        var picker1 = $('#selectWorkDatetime').datetimepicker({
            format: 'YYYY-MM-DD',
            locale: moment.locale('zh-cn'),
        });
        picker1.on('dp.change', function (e) {
            var date1 = $('#selectWorkDatetime input').val()
            //query_date: date1
            var query_data = {
                query_date: date1
            }
            $.ajax({
                url: '/api/getUserList/',
                type: 'POST',
                data: query_data,
                success: function (data) {
                    var data_obj = JSON.parse(data)
                    $('#mytab2').bootstrapTable('load', data_obj)
                },
            })

        })


        $('#setUserWorkList').bootstrapTable({
            method: 'POST',
            striped: true, //是否显示行间隔色
            pageNumber: 1, //初始化加载第一页
            pagination: true,//是否分页
            sidePagination: 'client',//server:服务器端分页|client：前端分页
            pageSize: 5,//单页记录数
            pageList: [5, 10],//可选择单页记录数
            // showRefresh: true,//刷新按钮
            columns: [
                {
                    title: '工作id',
                    field: 'id',
                    sortable: true
                },
                {
                    title: '户名',
                    field: 'user_na',
                    sortable: true
                },
                {
                    title: '流程号',
                    field: 'process_no',
                }, {
                    title: '业务类型',
                    field: 'business_type',
                }, {
                    title: '操作',
                    field: '',
                    formatter: operation2
                },
            ]
        });

        function operation2(value, row, index) {
            var htm = '<button class="btn btn-success btn-sm" onclick="show_details(' + index + ')">\n' +
                '                                        详细\n' +
                '                                    </button>'
            return htm
        }


    });

    $('#Acceptance_time_div,#reply_time_div,#send_power_time_div,#design_send_time_div,#design_complete_time_div,#construction_send_time_div,#construction_complete_time_div,#release_time_div').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss',
        locale: moment.locale('zh-cn'),
    });
    $('#mytab2').bootstrapTable({
        method: 'POST',
        url: "/api/getUserList/",//请求路径
        striped: true, //是否显示行间隔色
        pageNumber: 1, //初始化加载第一页
        pagination: true,//是否分页
        sidePagination: 'client',//server:服务器端分页|client：前端分页
        pageSize: 10,//单页记录数
        pageList: [5, 10, 20, 30],//可选择单页记录数
        showRefresh: true,//刷新按钮
        columns: [
            {
                title: '用户id',
                field: 'id',
                sortable: true
            },
            {
                title: '用户名',
                field: 'user_name',
                sortable: true
            },
            {
                title: '任务数量',
                field: 'num_of_work',
            }, {
                title: '总结',
                field: 'conclusion',
            }, {
                title: '任务详情',
                field: '',
                formatter: operation
            },
        ]
    });

    function operation(value, row, index) {
        var htm = '<button class="btn btn-success btn-sm" onclick="detailed_pop_init(' + index + ')" data-toggle="modal" data-target="#detailed_list_pop2">\n' +
            '                                        详细\n' +
            '                                    </button>'
        return htm
    }

    $('#detailed_list_pop2 .alert_detail_model').click(function () {
        $("#detailed_pop2").modal("show");
        $("#detailed_list_pop2").modal("hide");

    });

    // $('#detailed_pop2').on('show.bs.modal', function () {
    //     $("#detailed_pop2").modal("show");
    //     $("#detailed_list_pop2").modal("hide");
    // })

    $('#detailed_pop2').on('hidden.bs.modal', function () {
        $("#detailed_pop2").modal("hide");
        $("#detailed_list_pop2").modal("show");
        $('#detailed_pop_form2 textarea,#detailed_pop_form2 input[name!="user_name"]').val('')
    })
    $("td,th").addClass("text-center");
}

let detailed_pop_init = function (index) {
    var row = $('#mytab2').bootstrapTable('getData')[index]
    $('#detailed_pop_form2 textarea,#detailed_pop_form2 input').val('')
    // $('#detailed_pop_form2 input[name="id"]').val(row['id'])
    $('#detailed_pop_form2 input[name="user_name"]').val(row['user_name'])
    var date1 = $('#selectWorkDatetime input').val()
    //query_date: date1
    var query_data = {
        user_name: row['user_name'],
        query_date: date1
    }
    $.ajax({
        url: '/api/getWorkListByName/',
        type: 'POST',
        data: query_data,
        success: function (data) {
            // console.log(data)
            var data_obj = JSON.parse(data)
            $('#setUserWorkList').bootstrapTable('load', data_obj)
            for (let i in data_obj) {
                $('#detailed_pop_form2 textarea[name="' + i + '"],input[name="' + i + '"]').val(row[i])
            }
        },
    })
}

let show_details = function (index) {
    var row = $('#setUserWorkList').bootstrapTable('getData')[index]
    console.log(row)
    for (let i in row) {
        if (row[i] != 'None')
            $('#detailed_pop_form2 textarea[name="' + i + '"],input[name="' + i + '"]').val(row[i])
    }
    $("#detailed_list_pop2").modal("hide");
    $('#detailed_pop2').modal('show')
}

let addUserTaskSubmit = function () {

    $('#detailed_pop_form2').submit()
    $('#detailed_pop2').modal('hide')
}

