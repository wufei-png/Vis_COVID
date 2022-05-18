//import * as echarts from 'echarts';
async function request(url) {
    try {
        const res = await fetch(url);
        const data = await res.json();
        return data;
    } catch (e) {
        throw e;
    }
}


var chinaPieces = [{
    min: 1000,
    max: 1000000,
    label: '大于等于1000人',
    color: '#372a28'
}, {
    min: 500,
    max: 999,
    label: '确诊500-999人',
    color: '#4e160f'
}, {
    min: 100,
    max: 499,
    label: '确诊100-499人',
    color: '#974236'
}, {
    min: 10,
    max: 99,
    label: '确诊10-99人',
    color: '#ee7263'
}, {
    min: 1,
    max: 9,
    label: '确诊1-9人',
    color: '#f5bba7'
}, {
    min: 0,
    max: 0,
    label: '无确诊',
    color: 'white'
}];


var st_china = () => {
    var myChart = echarts.init(document.getElementById('china-map'));
    var speed_slider = 200;
    const SPEED_MAX = 500;
    const SPEED_MIN = 25;

    let dates = [];
    let provinces = [];
    // Play button
    const playButton = document.querySelector('.play-button');
    // Slider
    const slider = document.querySelector('.slider');
    // Slider date
    const sliderDate = document.querySelector('.slider-date');
    let interval;
    var setclock = () => {
        clearInterval(interval);
        interval = setInterval(() => {
            slider.value++;
            var date = dates[slider.value];
            var datestring = date.slice(0, 4) + '/' + date.slice(5, 7) + '/' + date.slice(8);
            sliderDate.innerHTML = datestring;
            changeEcharts(dates[slider.value]);
            updateCounters(countries['中国'], dates[slider.value]);
            show_histogram(provinces, dates[slider.value]);
            show_pie(provinces, dates[slider.value]);
            if (+slider.value === dates.length - 1) {
                playButton.innerHTML = 'Play';
                clearInterval(interval);
            }
        }, speed_slider);
    }

    var init_speed_button = () => {
        var buttons = document.getElementsByClassName('speed');
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].setAttribute('index', i);
            buttons[i].addEventListener("click", speed_handle);
        }
    }
    var speed_handle = function() {
        speed_handle_this(this);
    }
    var speed_handle_this = (element) => {
        console.log('element', String(element.innerHTML) == '+')
        if (String(element.innerHTML) == '+') {
            if (speed_slider > SPEED_MIN) {
                speed_slider -= 25;
            }
        } else if (speed_slider < SPEED_MAX) {
            speed_slider += 25;
        }
        console.log('speed_slider', speed_slider)
        if (playButton.innerText == 'Pause') //实时更新
        {
            setclock();
        }
    }


    // 改变echarts
    async function changeEcharts(date) {
        var tmpSeriesData = [];
        provinces = await request('../../../../../gpx/spider丁香/data/china.json');
        for (var province in provinces) {
            var ser = {
                name: province,
                value: provinces[province][date]['currentConfirmedCount']
            };
            tmpSeriesData.push(ser);
        }
        var option = {
            visualMap: {
                type: 'piecewise',
                pieces: chinaPieces,
                textStyle: {
                    color: '#000000'
                },
                inRange: {
                    color: ['lightskyblue', 'yellow', 'orangered']
                },
                top: '50%'
            },
            tooltip: {
                trigger: 'item'
            },
            series: [{
                name: '每日新增',
                type: 'map',
                mapType: 'china',
                roam: true,
                label: {
                    normal: {
                        show: false
                    },
                    emphasis: {
                        show: false
                    }
                },
                data: tmpSeriesData, //需要修改
                top: "3%" //组件距离容器的距离
            }]
        };
        myChart.setOption(option);
    }

    function init() {
        var date = '2022-05-04';
        changeEcharts(date);
        getCases(date); //调用这个更新时间跨度
        // init_change_button();
        init_speed_button();
    }
    init();

    async function getCases(date) {
        countries = await request('../../../../../gpx/spider丁香/data/world.json')
        provinces = await request('../../../../../gpx/spider丁香/data/china.json')
            //featureCollection = (await request(GEOJSON_URL)).features; //地图数据

        dates = Object.keys(countries['中国']);

        //   Set slider values
        slider.max = dates.length - 1;
        slider.value = dates.length - 1; //进度条

        slider.disabled = false; //为1无法拖动
        playButton.disabled = false;
        console.log(countries['中国']);
        updateCounters(countries['中国'], date);
        //updatePolygonsData();

        // updatePointOfView();
        show_histogram(provinces, date);
        show_pie(provinces, date);
    }
    const infectedEl = document.querySelector('#infected');
    const deathsEl = document.querySelector('#deaths');
    const recoveriesEl = document.querySelector('#recovered');
    const updatedEl = document.querySelector('.updated');

    function updateCounters(country, date) { //更新底部信息
        var date = date;
        var datestring = date.slice(0, 4) + '/' + date.slice(5, 7) + '/' + date.slice(8);
        sliderDate.innerHTML = datestring;

        infectedEl.innerHTML = country[date]['confirmedCount'];
        deathsEl.innerHTML = country[date]['deadCount'];
        recoveriesEl.innerHTML = country[date]['curedCount'];

        var datestring = date.slice(0, 4) + '/' + date.slice(5, 7) + '/' + date.slice(8);
        updatedEl.innerHTML = datestring;
    }

    playButton.addEventListener('click', () => {
        if (playButton.innerText === 'Play') {
            playButton.innerText = 'Pause';
        } else {
            playButton.innerText = 'Play';
            clearInterval(interval);
            return;
        }

        // Check if slider position is max
        if (+slider.value === dates.length - 1) {
            slider.value = 0; //在刚点击的时候是不是为最大值
        }

        sliderDate.innerHTML = dates[slider.value];

        setclock();
    });

    if ('oninput' in slider) { //指针滑动时间轴
        // console.log(666)
        slider.addEventListener(
            'input',
            function() {
                changeEcharts(dates[slider.value])
                updateCounters(countries['中国'], dates[slider.value]);
                //updatePolygonsData();
                show_histogram(provinces, dates[slider.value])
                show_pie(provinces, dates[slider.value]);
            },
            false
        );
    }


    function show_histogram(provinces, date) {

        var option = {
            backgroundColor: 'rgba(207,176,18,0)',
            title: {
                text: "现存确诊省份TOP5",
                padding: [20, 0, 0, 40],
                textStyle: {
                    color: 'white',
                },
                left: 'left'
            },
            color: ['#db3333'],
            tooltip: {
                trigger: 'axis',
                //指示器
                axisPointer: {
                    type: 'shadow'
                }
            },
            xAxis: {
                type: 'category',
                data: [],
                axisLabel: {
                    color: 'white',
                }
            },
            yAxis: {
                type: 'value',
                scale: true,
            },


            series: [{
                data: [],
                type: 'bar',
                barMaxWidth: "50%"
            }]
        };

        var topData = [];
        for (var key in provinces) {
            topData.push({
                'name': key,
                'value': provinces[key][date]['currentConfirmedCount']
            });
        }

        //降序排列
        topData.sort(function(a, b) {
            return b.value - a.value;
        });
        //只保留前10个
        topData.length = 5;
        //分别取出省份名称和数值
        for (var province of topData) {
            option.xAxis.data.push(province.name);
            option.series[0].data.push(province.value);
        }
        histogram.setOption(option);
    }

    function show_pie(provinces, date) {
        var option = {
            backgroundColor: 'rgba(166,207,18,0)',
            title: {
                // text: '现存确诊省份TOP5',
                // left: 'center',
                // textStyle: {
                //     fontSize: 20,
                //     fontWeight: 'bold',
                //     fontFamily: 'Microsoft YaHei',
                //     color: 'white'
                // },
            },
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b} : {c} ({d}%)'
            },
            legend: {
                padding: [100, 0, 0, 0],
                orient: 'vertical',
                left: 'right',
                data: [],
            },
            series: [{
                name: '省份名称',
                type: 'pie',
                radius: '55%',
                data: [],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0,0,0,0)'
                    }
                }
            }]
        };

        var topData = [];
        for (var key in provinces) {
            topData.push({
                'name': key,
                'value': provinces[key][date]['currentConfirmedCount']
            });
        }
        //降序的排列
        topData.sort(function(a, b) {
            return b.value - a.value;
        });
        //只保留前5个
        topData.length = 5;
        //分别取出省份名称和数据
        for (var country of topData) {
            option.legend.data.push(country.name);
            option.series[0].data.push(country);
        }
        pie.setOption(option);
    }

    var histogram = echarts.init(document.getElementById('histogram'), 'dark');
    var pie = echarts.init(document.getElementById('pie'), 'dark');
}
st_china();
/////////////////////////////////////////////////////////////////////////////