// $(function () { $('#collapseOne').collapse('hide')});

window.onload = function () {
    $(function () {
        var picker1 = $('#datetimepicker2').datetimepicker({
            format: 'YYYY-MM-DD',
            locale: moment.locale('zh-cn'),
        });
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
                title: 'id',
                field: 'id',
                sortable: true
            },
            {
                title: '用户名',
                field: 'name',
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
                title: '受理时间',
                field: 'Acceptance_time',
            }, {
                title: '送电时间',
                field: 'send_power_time',
            }, {
                title: '地址',
                field: 'address',
            }, {
                title: '详情',
                field: '',
                formatter: operation
            },
        ]
    });

    function operation(value, row, index) {
        var htm = '<button class="btn btn-success btn-sm" onclick="detailed_pop_init(' + index + ')" data-toggle="modal" data-target="#detailed_pop">\n' +
            '                                        详细\n' +
            '                                    </button>'
        return htm

    }

    $("td,th").addClass("text-center");
}

