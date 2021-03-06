//只是一个示例，用了随机数，等接入数据后修改
function randomData() {
    return Math.round(Math.random() * 500);
}

var mydata = [
    { name: '北京', value: randomData() },
    { name: '天津', value: randomData() },
    { name: '上海', value: randomData() },
    { name: '重庆', value: randomData() },
    { name: '河北', value: randomData() },
    { name: '河南', value: randomData() },
    { name: '云南', value: randomData() },
    { name: '辽宁', value: randomData() },
    { name: '黑龙江', value: randomData() },
    { name: '湖南', value: randomData() },
    { name: '安徽', value: randomData() },
    { name: '山东', value: randomData() },
    { name: '新疆', value: randomData() },
    { name: '江苏', value: randomData() },
    { name: '浙江', value: randomData() },
    { name: '江西', value: randomData() },
    { name: '湖北', value: randomData() },
    { name: '广西', value: randomData() },
    { name: '甘肃', value: randomData() },
    { name: '山西', value: randomData() },
    { name: '内蒙古', value: randomData() },
    { name: '陕西', value: randomData() },
    { name: '吉林', value: randomData() },
    { name: '福建', value: randomData() },
    { name: '贵州', value: randomData() },
    { name: '广东', value: randomData() },
    { name: '青海', value: randomData() },
    { name: '西藏', value: randomData() },
    { name: '四川', value: randomData() },
    { name: '宁夏', value: randomData() },
    { name: '海南', value: randomData() },
    { name: '台湾', value: randomData() },
    { name: '香港', value: randomData() },
    { name: '澳门', value: randomData() }
];

var option = {
    backgroundColor: '#e5f3fb',
    title: {
        text: '全国疫情地图',
        subtext: '数据未接入',
        x: 'center',
        textStyle: {
            color: '#074f73'
        }
    },
    tooltip: {
        trigger: 'item'
    },
    visualMap: {
        show: true,
        x: 'left',
        y: 'bottom',
        splitList: [
            { start: 500, end: 600 }, { start: 400, end: 500 },
            { start: 300, end: 400 }, { start: 200, end: 300 },
            { start: 100, end: 200 }, { start: 0, end: 100 },
        ],
        color: ['#074f73', '#176b95', '#3b8bb4', '#63add2', '#87ccef', '#c0dae7']
    },
    series: [{
        name: '当日新增',
        type: 'map',
        mapType: 'china',
        roam: false,
        label: {
            normal: {
                show: false
            },
            emphasis: {
                show: false
            }
        },
        data: mydata
    }]
};
var chart = echarts.init(document.getElementById('chinaMap'));
chart.setOption(option);